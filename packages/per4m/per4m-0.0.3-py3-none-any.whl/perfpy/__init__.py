from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution("perfpy").version
except DistributionNotFound:
     # package is not installed
    pass