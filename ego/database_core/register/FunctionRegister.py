from importlib import import_module
from functools import wraps

from ego.utils.file.File import query_file_name_list
from ego.classloader.base.BaseLoader import BaseLoader


class FunctionRegister(BaseLoader):
    def __init__(self, base_load_path):
        super().__init__(base_load_path)

    def __call__(self, func):
        self.func = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.scanner()
            self.load()

            return func(*args, **kwargs)

        return wrapper

    def scanner(self):
        if not self.import_all:
            return

        self.class_names = query_file_name_list(
            root_path=self.real_path,
            exclude_folder=self._exclude_folder,
            exclude_name=self._exclude_name,
        )

    def load(self):
        for class_name in self.class_names:
            import_module(f"{self.base_load_path}.{class_name}", class_name)
