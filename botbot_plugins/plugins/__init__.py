import os
from importlib import import_module

def get_submodules(module_string):
    module = import_module(module_string)
    modules_dir = os.path.dirname(module.__file__)
    modules = []
    for module in os.listdir(modules_dir):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        modules.append(module[:-3])
    return modules

__all__ = get_submodules('botbot_plugins.plugins')
