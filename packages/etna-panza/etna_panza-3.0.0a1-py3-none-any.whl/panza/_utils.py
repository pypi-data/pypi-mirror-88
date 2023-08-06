from contextlib import contextmanager
import sys
from typing import List


@contextmanager
def augment_syspath(paths: List[str]):
    old_path = sys.path.copy()
    sys.path += paths
    try:
        yield
    finally:
        sys.path = old_path


@contextmanager
def scoped_module_imports():
    original_modules = sys.modules.copy()
    try:
        yield
    finally:
        for mod in sys.modules.copy():
            if mod not in original_modules:
                del sys.modules[mod]
