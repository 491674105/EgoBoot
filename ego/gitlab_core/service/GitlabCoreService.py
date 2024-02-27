from asyncio import run_coroutine_threadsafe
from asyncio import sleep as a_sleep
from time import sleep

from gitlab import Gitlab

from ego import applicationContext, ApplicationContext
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.coroutine.service.LoopCoreService import LoopCoreService
from ego.gitlab_core.client.GitlabClient import GitlabClient
from ego.listener.Event import Event
from ego.listener.Listener import Listener
from ego.listener.ListenerManager import ListenerManager

from ego.common.constant.config import Base

from ego.exception.type.NullPointException import NullPointException


class GitlabCoreService:
    def __call__(self, clazz):
        if "gitlab" not in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]:
            return clazz

        self.log = LoggerCoreService.get_logger_instance()

        GitlabCoreService.connect()

        run_coroutine_threadsafe(self.register_listen(), LoopCoreService.get_loop_instance())
        return clazz

    async def register_listen(self):
        while not hasattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY) \
                or not getattr(applicationContext, Base.DEFAULT_APP_LAUNCHED_KEY):
            await a_sleep(1)

        while ListenerManager.LAZY_LOAD_KEY not in applicationContext.lazy_module_launched \
                or not applicationContext.lazy_module_launched[ListenerManager.LAZY_LOAD_KEY]:
            await a_sleep(1)

        event = Event()
        event.handler_ = self.keepalive
        event.kwargs_ = {"gitlab_config": applicationContext.base_config[
            getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)
        ]["gitlab"]}
        listener = Listener()
        listener.event_ = event
        listener.listener_interval = 60
        applicationContext.listener_manager.register(listener)

    @staticmethod
    def keepalive(gitlab_config):
        if not hasattr(applicationContext, "gitlab") or not getattr(applicationContext, "gitlab"):
            gitlab_client_context = ApplicationContext()
            setattr(applicationContext, "gitlab", gitlab_client_context)
        else:
            gitlab_client_context = getattr(applicationContext, "gitlab")

        for attr in gitlab_config:
            if hasattr(gitlab_client_context, attr["name"]) and getattr(gitlab_client_context, attr["name"]):
                continue

            gitlab_client = GitlabClient(url=attr["url"], token=attr["token"], self_hosted=attr["self_hosted"])
            gitlab_client.update(attr)
            gitlab_client.auth()
            setattr(gitlab_client_context, attr["name"], gitlab_client)

    @staticmethod
    def connect():
        gitlab_client_context = ApplicationContext()
        setattr(applicationContext, "gitlab", gitlab_client_context)
        for attr in applicationContext.base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["gitlab"]:
            gitlab_client = GitlabClient(url=attr["url"], token=attr["token"], self_hosted=attr["self_hosted"])
            gitlab_client.update(attr)
            gitlab_client.auth()
            setattr(gitlab_client_context, attr["name"], gitlab_client)

    @staticmethod
    def get_gitlab_instance(key=None) -> GitlabClient:
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not hasattr(applicationContext, "gitlab") or not getattr(applicationContext, "gitlab"):
            raise NullPointException("can not find the gitlab instance.")

        gitlab_instances = getattr(applicationContext, "gitlab")
        if not key or key == "":
            inst_name = "gitlab_main"
        else:
            inst_name = key

        if not hasattr(gitlab_instances, inst_name):
            sleep(10)
            if not hasattr(gitlab_instances, inst_name):
                GitlabCoreService.connect()
        return getattr(gitlab_instances, inst_name)

    @staticmethod
    def get_gitlab_real_instance(key=None) -> Gitlab:
        gitlab_instance = GitlabCoreService.get_gitlab_instance(key=key)

        return getattr(gitlab_instance, "gl_inst")
