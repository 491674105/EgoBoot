#!/usr/bin/env python3

from os import environ

from ego.common.constant.config import Base
from ego.common.enum.system.SysEnv import SysEnv

from ego.command.base.CommandExecutor import CommandExecutor
from ego.bootstrap.starter.Starter import Starter


def starter_hosting(service_name):
    environ[Base.DEFAULT_HOSTING_KEY] = SysEnv.HOSTING_OPEN.value
    environ[Base.DEFAULT_RUNNING_MODE_KEY] = SysEnv.RUNNING_MODE_SERVER.value
    starter_service = Starter()
    return starter_service.start_up(service_name=service_name)


if __name__ == "__main__":
    executor = CommandExecutor("ego.command")
    executor.scanner()
    executor.load()
