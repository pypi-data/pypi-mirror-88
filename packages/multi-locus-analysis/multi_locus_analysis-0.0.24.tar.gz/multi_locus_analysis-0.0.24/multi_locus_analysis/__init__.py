"""Module for fitting multi-particle stuff."""
from .stats import *
from .plotting import *
from .dataframes import *


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
