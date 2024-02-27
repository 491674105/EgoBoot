from os import listdir
from importlib import import_module

from ego.classloader.base.Loader import Loader

from ego.utils.file.File import path_format, get_path, package_format
from ego.exception.type.NullPointException import NullPointException


class ApplicationLoader(Loader):
    def __init__(self, service_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.root_path = path_format(f"{get_path()}")

        self.app_class = None
        if service_name:
            self.service_name = service_name

    def scanner(self):
        for file in listdir(self.root_path):
            name = file.split('_service')[0]
            if "_service" not in file or name != self.service_name:
                continue

            class_name = f"{name.upper()}Application"
            package_path = package_format(f"{self.root_path}{file}/{class_name}")
            clazz = getattr(import_module(package_path), class_name)
            self.app_class = clazz

    def load(self):
        if not self.app_class:
            raise NullPointException("No valid application was found!")

        app_inst = self.app_class()
        return app_inst.run()

    def query(self):
        no_match_flag = True
        for file in listdir(self.root_path):
            name = file.split('_service')[0].lower()
            if "_service" in file and name.find(self.service_name) != -1:
                no_match_flag = False
                print(f"service: {name}, start_cmd: /usr/bin/env python3 starter.py -s {name}")
        if no_match_flag:
            print("no matching service is found.")

    def query_all(self):
        no_match_flag = True
        for file in listdir(self.root_path):
            name = file.split('_service')[0].lower()
            if "_service" in file:
                no_match_flag = False
                print(f"service: {name}, start_cmd: /usr/bin/env python3 starter.py -s {name}")
        if no_match_flag:
            print("do not have any service.")
