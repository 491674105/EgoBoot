from argparse import ArgumentParser

from importlib import import_module

from ego.utils.file.File import query_file_name_list
from ego.classloader.base.BaseLoader import BaseLoader

from ego.utils.file.File import path_format, get_path


class CommandExecutor(BaseLoader):
    def __init__(self, base_load_path, import_all=True):
        super().__init__(base_load_path, import_all=import_all)
        self.root_path = path_format(f"{get_path()}")

    def scanner(self, *args, **kwargs):
        self._exclude_folder.append("base")

        self.class_names = query_file_name_list(
            root_path=self.real_path,
            exclude_folder=self._exclude_folder,
            exclude_name=self._exclude_name,
        )

    def load(self, *args, **kwargs):
        parser = ArgumentParser(*args, **kwargs)
        subparsers = parser.add_subparsers()

        for class_name in self.class_names:
            clazz = getattr(import_module(f"{self.base_load_path}.{class_name}"), class_name)
            subparser_name = class_name.replace("CommandExecutor", "").lower()
            inst = clazz(parser)
            inst.create_parser(subparsers.add_parser(name=subparser_name))
        args = parser.parse_args()
        args.func(args)
