from importlib import import_module
from functools import wraps

from ego.classloader.base.Loader import Loader


class DispatcherLoader(Loader):
    def __init__(self, package_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clazz = None
        self.clazz_name = None
        self.package_path = package_path

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.scanner()
            self.load()

            return func(*args, **kwargs)

        return wrapper

    def scanner(self):
        self.clazz_name = self.package_path.rsplit('.', 1)[1]

    def load(self):
        self.clazz = getattr(import_module(self.package_path), self.clazz_name)
        self.clazz()
