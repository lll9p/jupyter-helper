#!/usr/bin/env python3
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("helper")
except PackageNotFoundError:
    __version__ = "unknown version"


from .helper import Helper
