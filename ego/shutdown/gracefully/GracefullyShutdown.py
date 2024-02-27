from typing import Union
from logging import Logger

from os import getpid
from sys import exit

from signal import signal
from signal import SIGTERM
try:
    from signal import SIGHUP

    sig_hup_flag = True
except Exception:
    sig_hup_flag = False

from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.coroutine.service.LoopCoreService import LoopCoreService
from ego.coroutine.asynchronous.AsyncCoroutine import AsyncCoroutine

from ego.exception.type.NullPointException import NullPointException

from ego.shutdown.Shutdown import Shutdown


class GracefullyShutdown(Shutdown):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log: Union[Logger, None] = None

    def register(self, signal_handlers=None):
        if signal_handlers:
            for signal_no in signal_handlers:
                signal(signal_no, signal_handlers[signal_no])
        else:
            signal(SIGTERM, self._shutdown)
            if sig_hup_flag:
                signal(SIGHUP, self._shutdown)

    def _shutdown(self, sig_no, stack_frame):
        if not self.log:
            self.log = LoggerCoreService.get_logger_instance()

        try:
            loop_thread: AsyncCoroutine = LoopCoreService.get_loop_thread()
            loop_thread.stop()
        except NullPointException as e:
            self.log.error("Unable to close empty object.")
            self.log.error(e)

        self.log.warning(f"receive the {sig_no} signal number.")
        self.log.warning(f"The {getpid()} process is stopping.")
        try:
            exit(0)
        except Exception as e:
            self.log.error(e)
            self.log.exception(e)

    def exception_handler(self, e_type, e_value, e_traceback):
        if not self.log:
            self.log = LoggerCoreService.get_logger_instance()

        self.log.warning(f"this is {e_type}.")
        self.log.warning(f"the exception tell us {e_value}.")
        self.log.exception(e_traceback)
