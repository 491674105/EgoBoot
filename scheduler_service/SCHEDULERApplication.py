from os import getcwd
from flask_sqlalchemy import SQLAlchemy

from ego.bootstrap.application.base.BaseApplication import BaseApplication

from nacos_service.config.NacosFlaskConfig import NacosFlaskConfig
from nacos_service.NacosFlaskApplication import NacosFlaskApplication
from ego.classloader.DispatcherLoader import DispatcherLoader
from ego.classloader.ControllerLoader import ControllerLoader


@NacosFlaskApplication(__name__, SQLAlchemy(), root_path=getcwd())
@NacosFlaskConfig()
class SCHEDULERApplication(BaseApplication):
    @DispatcherLoader("ego.dispatch.Dispatcher")
    @ControllerLoader("scheduler_service.controller")
    def run(self):
        app = super().run()
        if app:
            return app

        self.create_server()
        self.server.serve_forever()
