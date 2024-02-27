from sys import modules
from importlib import import_module


def import_package_or_cls(package: str, cls_name: str = None):
    if package not in modules:
        this_module = import_module(package)
    else:
        this_module = modules[package]

    if not cls_name and cls_name != "":
        return getattr(this_module, cls_name)

    return this_module
