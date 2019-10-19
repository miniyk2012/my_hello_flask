import os
import sys


def here(module_name):
    """返回module所在目录"""
    return os.path.abspath(os.path.dirname(sys.modules[module_name].__file__))
