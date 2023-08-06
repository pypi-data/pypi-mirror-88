"""Get youtube video information and download links by url!"""

from . import types
from .exceptions import VideoNotAvailableException, WrongUrlException
from .yutubeless import search_async, search


__version__ = '1.0'

__all__ = [
    search, search_async,
    types,
    VideoNotAvailableException, WrongUrlException
]
