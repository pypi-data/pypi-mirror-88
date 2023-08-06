import importlib.machinery
import os as _os
import sys
from typing import List


def _path_stat(path):
    """Stat the path.

    Made a separate function to make it easier to override in experiments
    (e.g. cache stat results).

    """
    return _os.stat(path)


def _path_is_mode_type(path, mode):
    """Test whether the path is the specified mode type."""
    try:
        stat_info = _path_stat(path)
    except OSError:
        return False
    return (stat_info.st_mode & 0o170000) == mode


def _path_isdir(path):
    """Replacement for os.path.isdir."""
    if not path:
        path = _os.getcwd()
    return _path_is_mode_type(path, 0o040000)


class FileFinderLimited(importlib.machinery.FileFinder):
    """ a finder which limit search range in user-defined directories.
    for other project, default loader is used.
    """
    @classmethod
    def path_hook(cls, limited_dirs: List[str], *loader_details):
        """A class method which returns a closure to use on sys.path_hook
        which will return an instance using the specified loaders and the path
        called on the closure.

        If the path called on the closure is not a directory, ImportError is
        raised.
        """
        def path_hook_for_FileFinder(path):
            """Path hook for importlib.machinery.FileFinder."""
            if not _path_isdir(path):
                raise ImportError('only directories are supported', path=path)
            found = False
            real = _os.path.realpath(path)
            for ldir in limited_dirs:
                realdir = _os.path.realpath(ldir)
                if real.startswith(realdir):
                    found = True
                    break
            if not found:
                raise ImportError('path not in limited dirs', path=path)
            return cls(path, *loader_details)

        return path_hook_for_FileFinder


OTHER_LOADERS = [(importlib.machinery.ExtensionFileLoader,
                  importlib.machinery.EXTENSION_SUFFIXES),
                 (importlib.machinery.SourcelessFileLoader,
                  importlib.machinery.BYTECODE_SUFFIXES)]
IS_INSTALLED = False


def install_custom_loader(limited_dirs: List[str], loader_cls):
    global IS_INSTALLED
    if not IS_INSTALLED:
        sys.path_hooks.insert(
            1,
            FileFinderLimited.path_hook(
                limited_dirs,
                (loader_cls, importlib.machinery.SOURCE_SUFFIXES),
                *OTHER_LOADERS))
        IS_INSTALLED = True
