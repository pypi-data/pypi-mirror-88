from my_pkg.my_pkg import add
from my_pkg.my_pkg import subtract

__all__ = ["add", "subtract"]

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
