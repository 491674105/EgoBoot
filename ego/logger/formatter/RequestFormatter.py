from logging import Formatter


class RequestFormatter(Formatter):
    __fmt_inst = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_formatter(self):
        return self.__fmt_inst
