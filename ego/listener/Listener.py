from logging import Logger

from ego.logger.service.LoggerCoreService import LoggerCoreService

from ego.listener.Event import Event

log: Logger


class Listener:
    """
        监听器
    """

    def __init__(self, listener_interval=-1, inner_id=None, event_: Event = None):
        self.__listener_interval = listener_interval

        self.__inner_id = inner_id

        self.__event: Event = event_

        global log
        log = LoggerCoreService.get_logger_instance()

    @property
    def listener_interval(self):
        return self.__listener_interval

    @listener_interval.setter
    def listener_interval(self, listener_interval):
        self.__listener_interval = listener_interval

    @property
    def inner_id(self):
        return self.__inner_id

    @inner_id.setter
    def inner_id(self, inner_id):
        self.__inner_id = inner_id

    @property
    def event_(self):
        return self.__event

    @event_.setter
    def event_(self, event_: Event):
        self.__event = event_

    def trigger(self):
        try:
            self.__event.handler_(*self.__event.args_, **self.__event.kwargs_)
        except Exception as e:
            log.exception(e)
