from os import path, listdir
from importlib import import_module

from ego.classloader.base.Loader import Loader

from ego.utils.file.File import path_format, get_path, package_format
from ego.utils.json.JSONUtil import sort_json


class ClassLoader(Loader):

    def __init__(self, base_path, root_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__default_order_id = 100
        self.__classes = {}

        self.base_path = base_path
        if root_path:
            self.base_path = path_format(f"{root_path}{base_path}")
        else:
            self.base_path = path_format(f"{get_path()}/{base_path}")

    def scanner(self):
        for file in listdir(self.base_path):
            file_attr = path.splitext(file)
            if file_attr[1] == ".py" and file_attr[0] != "__init__":
                class_name = file_attr[0]
                base_package = package_format(f"{self.base_path}.{class_name}")
                self.__create_class_dict(getattr(import_module(base_package), class_name))

    def load(self):
        self.scanner()
        return self.__classes

    def __create_class_dict(self, clazz):
        if clazz.order_id == -1:
            self.__default_order_id = self.__default_order_id - 1
            self.__classes[self.__default_order_id] = clazz
            return

        if clazz.order_id != -1 and clazz.order_id not in self.__classes:
            self.__classes[clazz.order_id] = clazz
            return

        self.__insert(clazz)

    def __insert(self, clazz):
        self.__classes = sort_json(self.__classes)
        classes_cache = {}
        for order_id in self.__classes:
            if order_id == clazz.order_id:
                index = clazz.order_id + 1
                classes_cache[index] = clazz
                continue

            if order_id in classes_cache:
                index = order_id + 1
                classes_cache[index] = self.__classes[order_id]
                continue

            classes_cache[order_id] = self.__classes[order_id]

        self.__classes = classes_cache
