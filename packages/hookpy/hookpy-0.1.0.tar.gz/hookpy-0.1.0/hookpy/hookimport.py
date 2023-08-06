import importlib.machinery
from typing import List

from hookpy import importer
from hookpy.core import register_hook
from hookpy.funcid import modify_func_of_file, parse_source_path


def _modifier(mod, key: str, set_attr_func):
    set_attr_func(key, register_hook(getattr(mod, key)))


class RegisterHookLoader(importlib.machinery.SourceFileLoader):
    def exec_module(self, module):
        res = super().exec_module(module)
        # generate ast, then register functions
        tree, _ = parse_source_path(self.path)
        modify_func_of_file(tree, module, _modifier)
        return res


def install_register_hook(limited_dirs: List[str]):
    return importer.install_custom_loader(limited_dirs, RegisterHookLoader)
