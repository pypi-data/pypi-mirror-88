from pkg_resources import get_distribution, DistributionNotFound
from setuptools_scm import get_version

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = get_version(root="..", relative_to=__file__)
