from typing import Union, Dict
from copy import copy

from queue import Queue
from threading import Thread
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from asyncio import run_coroutine_threadsafe
from asyncio import sleep as a_sleep

from ego import applicationContext
from ego.loader.LazyLoader import LazyLoader
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.coroutine.service.LoopCoreService import LoopCoreService

from ego.listener.Listener import Listener

from ego.utils.index.Index import get_for_unique_uuid


class ListenerManager:
    """
        监听管理
    """
    LAZY_LOAD_KEY = "listener_manager"

    # 默认事件监听间隔，默认：30s
    __DEFAULT_LISTENING_INTERVAL = 30
    # 默认线程池大小
    __DEFAULT_WORKS = 4

    def __init__(self, workers=0, lazy_load=True):
        # 懒加载开关
        self.__lazy_load = lazy_load

        # 管理器开关
        self.__active = False
        # 管理器进程
        self.__manager = Thread(target=self.__run)
        # 任务处理池
        if workers > 0:
            self.__job_process = ThreadPoolExecutor(workers)
        else:
            self.__job_process = ThreadPoolExecutor(self.__DEFAULT_WORKS)

        self.__job_queue = Queue()
        self.__running_job_set = set()

        # 监听器容器，以监听间隔为键对监听器进行分类保存
        self.__listener_map: Dict[int, dict] = {
            self.__DEFAULT_LISTENING_INTERVAL: {}
        }
        self.log = LoggerCoreService.get_logger_instance()

    @property
    def lazy_load(self):
        return self.__lazy_load

    @lazy_load.setter
    def lazy_load(self, lazy_load_):
        self.__lazy_load = lazy_load_

    def __call__(self, clazz):
        self.clazz = clazz

        if hasattr(applicationContext, "listener_manager"):
            return clazz
        listener_manager = ListenerManager()
        setattr(applicationContext, "listener_manager", listener_manager)

        if not self.__lazy_load:
            listener_manager.start()
            return clazz

        LazyLoader.commit_lazy_load_module(
            module_id=self.LAZY_LOAD_KEY,
            loader=listener_manager.start,
            args=[],
            kwargs={}
        )

        return clazz

    @classmethod
    def load(cls, **kwargs):
        if hasattr(applicationContext, "listener_manager"):
            return
        listener_manager = cls(**kwargs)
        setattr(applicationContext, "listener_manager", listener_manager)

        if not listener_manager.lazy_load:
            listener_manager.start()
            return

        LazyLoader.commit_lazy_load_module(
            module_id=cls.LAZY_LOAD_KEY,
            loader=listener_manager.start,
            args=[],
            kwargs={}
        )

    def register(self, listener: Listener):
        """
            监听器注册
            :return listener_id
        """
        try:
            listener_id = get_for_unique_uuid()
            listener.inner_id = listener_id
            if listener.listener_interval >= 0:
                if listener.listener_interval not in self.__listener_map:
                    listeners = {}
                    self.__listener_map[listener.listener_interval] = listeners

                self.__listener_map[listener.listener_interval][listener_id] = listener
                self.__job_queue.put(listener.listener_interval)
                return f"{listener.listener_interval}.{listener_id}"

            self.__listener_map[self.__DEFAULT_LISTENING_INTERVAL][listener_id] = listener
            self.__job_queue.put(listener.listener_interval)
            return f"{listener.listener_interval}.{listener_id}"
        except Exception as e:
            self.log.exception(e)

    def unregister(self, listener_id: str = None, listener: Union[Listener, None] = None):
        """
            取消监听器注册
        """
        if listener_id and listener_id != "":
            ids = listener_id.split(".")
            if not ids or len(ids) < 2:
                return False

            listener_interval = int(ids[0])
            inner_id = ids[1]
            del self.__listener_map[listener_interval][inner_id]
            return True

        if not listener.listener_interval or listener.listener_interval <= 0:
            return False
        if not listener.inner_id or listener.inner_id == "":
            return False

        del self.__listener_map[listener.listener_interval][listener.inner_id]
        return True

    def unregister_all(self):
        """
            清空管理器中的监听器实例
        """
        self.__listener_map.clear()
        self.__listener_map = {
            self.__DEFAULT_LISTENING_INTERVAL: {}
        }

    def __push_to_process(self, listener_interval):
        # self.log.debug("准备推送处理机......")
        interval_tmp = copy(listener_interval)
        count = 0
        while interval_tmp > 0:
            # self.log.debug(f"推送倒计时{interval_tmp}")
            sleep(1)
            interval_tmp -= 1
            count += 1
            if count not in self.__listener_map:
                continue
            run_coroutine_threadsafe(self.__trigger(count), LoopCoreService.get_loop_instance())
        self.__running_job_set.remove(listener_interval)
        self.__job_queue.put(listener_interval)

    def __run(self):
        """
            运行监听管理器核心模块
        """
        self.log.debug("准备启动监听管理......")
        if not self.__active:
            self.log.error("监听管理启动异常！")

        self.log.debug("管理器已启动。")
        while self.__active:
            # log.debug("正在检查监听管理环境......")
            sleep(1)
            if self.__lazy_load:
                if not hasattr(applicationContext, "app_launched") or not applicationContext.app_launched:
                    # self.log.debug("等待相关组件启动完成......")
                    continue

            while not self.__job_queue.empty():
                listener_interval = self.__job_queue.get()
                # self.log.debug(f"找到{listener_interval}类型的监听规则。")
                if listener_interval in self.__running_job_set:
                    # self.log.debug(f"类型{listener_interval}监听规则已处于运行状态。")
                    continue

                # self.log.debug(f"正在启动类型{listener_interval}监听规则......")
                self.__running_job_set.add(listener_interval)
                self.__job_process.submit(self.__push_to_process(listener_interval))
                # self.log.debug(f"类型{listener_interval}监听规则已启动。")

        self.unregister_all()

    async def __trigger(self, listener_interval):
        """
            事件触发
        """
        await a_sleep(0.000001)
        listeners: Dict[str, Listener] = self.__listener_map[listener_interval]
        if not listeners:
            return

        for l_id in listeners:
            listener_ = listeners[l_id]
            listener_.trigger()

    def start(self):
        """
            外部启动入口
        """
        self.log.debug("正在初始化监听管理......")
        self.__active = True
        self.__manager.start()

    def stop(self):
        """
            外部停止入口
        """
        self.__active = False
        self.__manager.join()
