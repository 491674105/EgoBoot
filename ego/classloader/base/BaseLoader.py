from importlib import import_module

from ego.classloader.base.Loader import Loader


class BaseLoader(Loader):
    _exclude_folder = [".", "..", "__pycache__"]
    _exclude_name = ["__init__"]
    _exclude_type = [""]

    def __init__(self, base_load_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_load_path = base_load_path

        if self.base_load_path.find(".*") == len(self.base_load_path) - 2 \
                or ("import_all" in kwargs and kwargs["import_all"]):
            self.import_all = True
            self.base_load_path = self.base_load_path.replace(".*", "")
            self.base_load_packages = import_module(self.base_load_path)
            self.class_names = []
        else:
            self.import_all = False
            self.base_load_packages = None
            self.class_names = [self.base_load_path.split(".")[-1]]

        # noinspection PyBroadException
        try:
            self.real_path = self.base_load_packages.__path__[0]
        except Exception:
            # 兼容python3.7及以下版本
            self.real_path = getattr(self.base_load_packages.__path__, "_path")[0]

    def scanner(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass
