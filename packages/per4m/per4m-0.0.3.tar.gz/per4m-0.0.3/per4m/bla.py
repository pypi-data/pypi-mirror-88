import argparse
import argparse
from collections import defaultdict
import json
import sys

import tabulate

from .perfutils import read_events

def parse_values(parts, **types):
    values = {}
    for part in parts:
        if "=" in part:
            key, value = part.split('=', 1)
            value = types.get(key, str)(value)
            values[key] = value
    for key in types:
        if key not in values:
            raise ValueError(f'Expected to find key {key} in {parts}')
    return values


def in_stacktrace(function_name, stacktrace):
    return any(function_name in call for call in stacktrace)


def takes_gil(stacktrace):
    return in_stacktrace('take_gil', stacktrace)


def drops_gil(stacktrace):
    return in_stacktrace('drop_gil', stacktrace)


usage = """

Convert perf.data to TraceEvent JSON data.

Usage for scheduling data:

Always run perf with -e 'sched:*' --call-graph dwarf -k CLOCK_MONOTONIC, the rest of the events are extra
$ perf record -e 'sched:*' --call-graph dwarf -k CLOCK_MONOTONIC -e L1-dcache-load-misses -e instructions -e cycles -e page-faults -- python -m per4m.example1 
Run with --no-online, otherwise it may run slow
$ perf script --no-inline | per4m perf2trace sched --no-running -o example1sched.json
$ viztracer --combine example1sched.json example1perf.json -o example1.html

Usage for GIL:

(read the docs to install the GIL uprobes)
$ perf record -e 'python:*gil*' -k CLOCK_MONOTONIC -- python -m per4m.example1
$ perf script --no-inline | per4m perf2trace gil -o example1gil.json
$ viztracer --combine example1.json example1gil.json -o example1.html


"""

def main(argv=sys.argv):
    parser = argparse.ArgumentParser(argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=usage)
    parser.add_argument('--verbose', '-v', action='count', default=1)
    parser.add_argument('--quiet', '-q', action='count', default=0)
    parser.add_argument('--sleeping', help="store sleeping phase (default: %(default)s)", default=True, action='store_true')
    parser.add_argument('--no-sleeping', dest="sleeping", action='store_false')
    parser.add_argument('--running', help="show running phase (default: %(default)s)", default=False, action='store_true')
    parser.add_argument('--no-running', dest="running", action='store_false')
    parser.add_argument('--as-async', help="show as async (above the events) (default: %(default)s)", default=True, action='store_true')
    parser.add_argument('--no-as-async', dest="as_async", action='store_false')
    parser.add_argument('--only-lock', help="show only when we have the GIL (default: %(default)s)", default=False, action='store_true')
    parser.add_argument('--no-only-lock', dest="as_async", action='store_false')
    parser.add_argument('--all-tracepoints', help="store all tracepoints phase (default: %(default)s)", default=False, action='store_true')

    parser.add_argument('--input', '-i', help="Optional VizTracer input for filtering and gil load calculations")

    parser.add_argument('--output', '-o', dest="output", default='perf.json', help="Output filename (default %(default)s)")
    parser.add_argument("type", help="Type of conversion to do", choices=['sched', 'gil'])


    args = parser.parse_args(argv[1:])
    verbose = args.verbose - args.quiet
    store_runing = args.running
    store_sleeping = args.sleeping

    trace_events = []
    if args.type == "sched":
        for header, tb, event in perf2trace(sys.stdin, verbose=verbose, store_runing=store_runing, store_sleeping=store_sleeping, all_tracepoints=args.all_tracepoints):
            trace_events.append(event)
    elif args.type == "gil":
        t_min = {}
        t_max = {}
        if args.input:
            with open(args.input) as f:
                input_events = json.load(f)['traceEvents']
            for event in input_events:
                if 'ts' in event:
                    ts = event['ts']
                    pid = int(event['tid'])
                    t_min[pid] = min(t_min.get(pid, ts), ts)
                    t_max[pid] = max(t_max.get(pid, ts), ts)

        for header, event in gil2trace(sys.stdin, verbose=verbose, as_async=args.as_async, only_lock=args.only_lock, t_min=t_min, t_max=t_max):
            if verbose >= 3:
                print(event)
            trace_events.append(event)
    else:
        raise ValueError(f'Unknown type {args.type}')
    with open(args.output, 'w') as f:
        json.dump({'traceEvents': trace_events}, f)
    if verbose >= 1:
        print(f"Wrote to {args.output}")


def gil2trace(input, verbose=1, take_probe="python:take_gil(_\d)?$", take_probe_return="python:take_gil__return", drop_probe="python:drop_gil(_\d)?$", drop_probe_return="python:drop_gil__return", as_async=False, show_instant=True, duration_min_ns=1, only_lock=True, t_min={}, t_max={}):
    time_first = None
    # dicts: pid -> time
    wants_take_gil = {}
    wants_drop_gil = {}
    has_gil = {}
    parent_pid = None
    ignored = set()
    time_on_gil = defaultdict(int)
    # time_off_gil = defaultdict(int)
    time_wait_gil = defaultdict(int)
    import re
    for header in input:
        try:
            header = header.strip()
            if verbose >= 2:
                print(header)

            # parse the header
            comm, pid, cpu, time, event, *other = header.split()
            pid = int(pid)
            if parent_pid is None:  # lets assume the first event is from the parent process
                parent_pid = pid
            assert event[-1] == ':'
            event = event[:-1]  # take off :
            assert time[-1] == ':'
            time = time[:-1]  # take off :
            time = float(time[:-1]) * 1e6
            
            # optionally filter by min and max time
            # if time <= t_min.get(pid, time):
            #     continue
            # if time >= t_max.get(pid, time):
            #     continue

            # and proces it
            if time_first is None:
                time_first = time

            if re.match(take_probe, event):
                wants_take_gil[pid] = time
            elif re.match(drop_probe, event):
                wants_drop_gil[pid] = time
            elif re.match(take_probe_return, event):
                if has_gil:
                    for conflict_pid in has_gil:
                        overlap = time - has_gil[conflict_pid]
                        if overlap > 6000: # this many ns overlap is ok
                            # I think it happens when a thread has dropped the GIL, but it has not returned yet
                            # TODO: we should be able to correct the times
                            tip = "(If running as giltracer, try passing --no-state-detect to reduce CPU load"
                            print(f'Anomaly: PID {conflict_pid} already seems to have the GIL, {overlap} ns overlap) {tip}', file=sys.stderr)
                    # has_gil = {}
                has_gil[pid] = time
                time_wait_gil[pid] += time - wants_take_gil[pid]
                # if as_event:
            elif re.match(drop_probe_return, event):
                if pid not in has_gil:
                    print(f'Anomaly: this PIDs drops the GIL: {pid}, but never took it (maybe we missed it?)', file=sys.stderr)
                    # continue
                time_gil_take = has_gil.get(pid, time_first)
                time_gil_drop = time
                duration = time_gil_drop - time_gil_take
                time_on_gil[pid] += duration
                if pid in has_gil:
                    del has_gil[pid]
                # print(duration)
                if duration < duration_min_ns:
                    if verbose >= 2:
                        print(f'Ignoring {duration}ns duration GIL lock', file=sys.stderr)
                    continue

                args = {'duraction': f'{duration} ns'}
                if show_instant:
                    # we do both tevent only after drop, so we can ignore 0 duraction event
                    # TODO: 'flush' out takes without a drop (e.g. perf stopped before drop happned)
                    name = "GIL-take"
                    scope = "t"  # thread scope
                    event = {"pid": parent_pid, "tid": f'{pid}', "ts": time_gil_take, "name": name, "ph": "i", "cat": "GIL state", 's': scope, 'cname': 'terrible'}
                    yield header, event

                    name = "GIL-drop"
                    scope = "t"  # thread scope
                    event = {"pid": parent_pid, "tid": f'{pid}', "ts": time_gil_drop, "name": name, "ph": "i", "cat": "GIL state", 's': scope, 'args': args, 'cname': 'good'}
                    yield header, event

                if as_async:
                    begin, end = 'b', 'e'

                else:
                    begin, end = 'B', 'E'
                event_id = int(time*1e3)
                # begin, end = 's', 'f'
                name = "GIL-flow"
                common = {"pid": parent_pid if as_async else f'{parent_pid}-GIL', "tid": f'{pid}', 'cat': 'GIL state', 'args': args, 'id': event_id, 'cname': 'terrible'}
                # we may have called take_gil ealrier than we got it back
                # sth like [called take [ take success [still dropping]]]
                if not only_lock and pid in wants_take_gil:
                    yield header, {"name": 'GIL(take)', "ph": begin, "ts": wants_take_gil[pid], **common, 'cname': 'bad'}
                yield header, {"name": 'GIL',   "ph": begin, "ts": time_gil_take, **common}
                if not only_lock:
                    yield header, {"name": 'GIL(drop)',   "ph": begin, "ts": wants_drop_gil[pid], **common}
                    yield header, {"name": 'GIL(drop)', "ph": end, "ts": time_gil_drop, **common}
                yield header, {"name": 'GIL', "ph": end, "ts": time_gil_drop, **common}
                if not only_lock and pid in wants_take_gil:
                    yield header, {"name": 'GIL(take)', "ph": end, "ts": time_gil_drop, **common, 'cname': 'bad'}
            else:
                if event not in ignored:
                    print(f'ignoring {event}', file=sys.stderr)
                    ignored.add(event)
        except:
            print("error on line", header, file=sys.stderr)
            raise
    if verbose >= 1:
        print("Summary of threads: (other time includes sleeping)")
        pids = ["PID"]
        totals = ["total"]
        wait = ["wait"]
        table = []
        for pid in t_min:
            total = t_max[pid] - t_min[pid]
            wait = time_wait_gil[pid]
            on_gil = time_on_gil[pid]
            misc = total - wait - on_gil
            table.append([pid, total, wait, wait/total * 100, on_gil, on_gil/total*100, misc, misc/total*100])
        # table = tabulate.tabulate([pids, totals], tablefmt="grid")
        headers = ['PID', 'total', 'wait', 'wait%', 'on gil', 'on gil%', 'other', 'other%']
        table = tabulate.tabulate(table, headers)#, tablefmt="grid")
        print()
        print(table)
            # print(f'PID {pid} was active  ")
            # wait = time_wait_gil[pid]
        # yield '', {"cat": "foo", "name": "async_read", "id": 0x100, "ph": "b", "args": {"name" : "~/.bashrc"}},
        # yield '', {"cat": "foo", "name": "async_read", "id": 0x100, "ph": "e"}


def perf2trace(input, verbose=1, store_runing=False, store_sleeping=True, all_tracepoints=False):
    # useful for debugging, to have the pids a name
    pid_names = {}
    # pid_names = {872068: "main", 872070: "t1", 872071: "t2"}
    # a bit pendantic to keep these separated
    last_run_time = {}
    last_sleep_time = {}
    last_sleep_stacktrace = {}
    time_first = None
    parent_pid = {}  # maps pid/tid to the parent
    count = None
    for header, stacktrace in read_events(input):
        try:
            if verbose >= 3:
                print(header)
            pid = None
            parts = header.split()
            # python 302629 [011] 3485124.180312:       sched:sched_switch: prev_comm=python prev_pid=302629 prev_prio=120 prev_state=S ==> next_comm=swapper/11 next_pid=0 next_prio=120
            event = parts[4][:-1] # strip off ':'
            if ":" in event:  # tracepoint
                dso, triggerpid, cpu, time, _, *other = parts
                tracepoint = True
            else:  # counter etc
                dso, triggerpid, time, count, _, *other = parts
                tracepoint = False
            triggerpid = int(triggerpid)
            time = float(time[:-1]) * 1e6
            if time_first is None:
                time_first = time
            def log(*args, time=time/1e6):
                offset = time - time_first/1e6
                print(f"{time:13.6f}[+{offset:5.4f}]", *args)
            if all_tracepoints and tracepoint:
                yield header, stacktrace, {'name': event, 'pid': parent_pid.get(pid, pid), 'tid': triggerpid, 'ts': time, 'ph': 'i', 's': 'g'}
            first_line = False
            gil_event = None
            if event == "sched:sched_switch":
                # e.g. python 393320 [040] 3498299.441431:                sched:sched_switch: prev_comm=python prev_pid=393320 prev_prio=120 prev_state=S ==> next_comm=swapper/40 next_pid=0 next_prio=120
                try:
                    values = parse_values(parts, prev_pid=int)
                    pid = values['prev_pid']
                    prev_state = values['prev_state']
                except ValueError:
                    # perf 4
                    comm, pid = other[0].rsplit(':', 1)
                    pid = int(pid)
                    prev_state = other[2]
                # we are going to sleep?
                if prev_state == 'R':
                    # this happens when a process just started, so we just set the start time
                    last_sleep_time[pid] = time
                    continue
                # if values['prev_comm'] != "python":
                #     if verbose >= 2:
                #         log(f'Skipping switch from {values["prev_comm"]}')
                name = pid_names.get(pid, pid)
                if pid not in last_run_time:
                    # raise ValueError(f'pid {pid} not seen running before, only {last_run_time}')
                    continue
                dur = time  - last_run_time[pid]
                if verbose >= 2:
                    log(f'{name} will switch to state={prev_state}, ran for {dur}')
                if store_runing:
                    event = {"pid": parent_pid.get(pid, pid), "tid": pid, "ts": last_run_time[pid], "dur": dur, "name": 'R', "ph": "X", "cat": "process state"}
                    yield header, stacktrace, event
                # print("SLEEP:", drops_gil(stacktrace), takes_gil(stacktrace))
                # print("   ", header)

                last_sleep_time[pid] = time
                last_sleep_stacktrace[pid] = stacktrace
                del last_run_time[pid]
            elif event == "sched:sched_wakeup":
                # e.g: swapper     0 [040] 3498299.642199:                sched:sched_waking: comm=python pid=393320 prio=120 target_cpu=040
                prev_state = None
                try:
                    values = parse_values(parts, pid=int)
                    pid = values['pid']
                    comm = values['comm']
                except ValueError:
                    # perf 4
                    comm, pid = other[0].rsplit(':', 1)
                    pid = int(pid)

                # if comm != "python":
                #     if verbose >= 2:
                #         log(f'Skip waking event for {comm}')
                #     continue
                if pid not in last_sleep_time:
                    # raise ValueError(f'pid {pid} not seen sleeping before, only {last_sleep_time}')
                    # this can happen when we did not see the creation
                    # q
                    last_run_time[pid] = time
                    continue
                recover_from_gil = takes_gil(last_sleep_stacktrace[pid])
                # if drops_gil(last_sleep_stacktrace[pid]):
                #     print("HOLY MOLY")
                #     print(header)
                duration = time  - last_sleep_time[pid]
                if verbose >= 2:
                    name = pid_names.get(pid, pid)
                    log(f'Waking up {name}', '(recovering from GIL)' if recover_from_gil else '', f', slept for {duration} msec')
                if verbose >= 3:
                    print("Stack trace when we went to sleep:\n\t", "\t".join(last_sleep_stacktrace[pid]))
                if store_sleeping:
                    if recover_from_gil:
                        name = 'S(GIL)'
                        cname = 'terrible'
                    else:
                        name = 'S'
                        cname = 'bad'
                    event = {"pid": parent_pid.get(pid, pid), "tid": pid, "ts": last_sleep_time[pid], "dur": duration, "name": name, "ph": "X", "cat": "process state", 'cname': cname}
                    # A bit ugly, but here we lie about the stacktrace, we actually yield the one that caused us to sleep (for offgil.py)
                    yield header, last_sleep_stacktrace[pid], event
                last_run_time[pid] = time
                del last_sleep_time[pid]
            elif event == "sched:sched_process_exec":
                if verbose >= 2:
                    name = pid_names.get(triggerpid, triggerpid)
                    log(f'Starting (exec) {name}')
            elif event == "sched:sched_wakeup_new":
                # e.g: swapper     0 [040] 3498299.642199:                sched:sched_waking: comm=python pid=393320 prio=120 target_cpu=040
                try:
                    values = parse_values(parts, pid=int)
                    pid = values['pid']
                except ValueError:
                    # perf 4
                    comm, pid = other[0].rsplit(':', 1)
                    pid = int(pid)
                if verbose >= 2:
                    name = pid_names.get(pid, pid)
                    log(f'Starting (new) {name}')
                last_run_time[pid] = time
            elif event == "sched:sched_process_fork":
                values = parse_values(parts, pid=int, child_pid=int)
                # set up a child parent relationship for better visualization
                pid, child_pid = values['pid'], values['child_pid']
                if verbose >= 2:
                    log(f'Process {pid} forked {child_pid}')
                parent_pid[child_pid] = pid
            elif not tracepoint:
                event = {"pid": 'counters', "ts": time, "name": event, "ph": "C", "args": {event: count}}
                yield header, stacktrace, event
            else:
                if verbose >= 2:
                    print("SKIP", header)
                pass
        except BrokenPipeError:
            break
        except:
            print("error on line", header, other, file=sys.stderr)
            raise


if __name__ == '__main__':
    main()
