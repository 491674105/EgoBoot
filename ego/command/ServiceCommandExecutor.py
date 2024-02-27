from os import environ
from os import getppid
from psutil import Process
from signal import SIGTERM

from argparse import ArgumentParser, Namespace

from ego.common.constant.config import Base
from ego.common.enum.system.SysEnv import SysEnv

from ego.bootstrap.starter.Starter import Starter


class ServiceCommandExecutor:
    def __init__(self, root_parser: ArgumentParser):
        self.root_parser = root_parser
        self.subparser = None
        self.starter = Starter()

    def create_parser(self, subparser: ArgumentParser):
        self.subparser = subparser
        subparser.add_argument(
            "-s",
            "--start",
            metavar="service_name",
            nargs="?",
            help="standalone service startup"
        )
        subparser.add_argument(
            "-q",
            "--query",
            metavar="keyword",
            nargs="?",
            help="query by [service_name]-keyword. "
        )
        subparser.add_argument("--query_all", default=False, action="store_true", help="view all services")
        subparser.set_defaults(func=self.executor)

    def executor(self, args: Namespace):
        for attr_name in args.__dict__:
            if hasattr(self, attr_name) and args.__dict__[attr_name] and args.__dict__[attr_name] != "":
                getattr(self, attr_name)(args)
                return

    def start(self, args):
        try:
            if Base.DEFAULT_HOSTING_KEY not in environ or environ[Base.DEFAULT_HOSTING_KEY] in (None, ""):
                environ[Base.DEFAULT_HOSTING_KEY] = SysEnv.HOSTING_CLOSE.value

            if Base.DEFAULT_RUNNING_MODE_KEY not in environ \
                    or environ[Base.DEFAULT_RUNNING_MODE_KEY] in (None, ""):
                environ[Base.DEFAULT_RUNNING_MODE_KEY] = SysEnv.RUNNING_MODE_DEVELOPER.value
            self.starter.start_up(service_name=args.start)
        except KeyboardInterrupt:
            Process(pid=getppid()).send_signal(SIGTERM)
            exit(0)

    def query(self, args):
        self.starter.query_service(args.query)

    def query_all(self):
        self.starter.query_all_service()
