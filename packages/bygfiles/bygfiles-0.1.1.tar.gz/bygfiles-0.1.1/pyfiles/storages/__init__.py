import sys
import importlib

from pyfiles.storages.diskstorage import DiskStorage
from pyfiles.storages.s3storage import S3Storage

__all__ = ['DiskStorage', 'S3Storage']


def get_storage(backend, options):
    module_path, _, clazz = backend.rpartition('.')
    try:
        module = importlib.import_module(module_path)
    except ImportError as exc:
        msg = str(exc)
        if 'No module' not in msg:
            print("IMPORT ERROR %s" % module)
            raise
        if module not in msg:
            print("IMPORT ERROR %s" % module)
            raise
        print("Missing '%s' module !" % module)
        raise
    else:
        return getattr(module, clazz)(**options)
