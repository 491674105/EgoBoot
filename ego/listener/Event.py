class Event:
    """
        事件实体
    """

    def __init__(self, handler=None, args=None, kwargs=None):
        self.__handler = handler

        if not args:
            self.__args = []
        else:
            self.__args = args

        if not kwargs:
            self.__kwargs = {}
        else:
            self.__kwargs = kwargs

    @property
    def handler_(self):
        return self.__handler

    @handler_.setter
    def handler_(self, handler):
        self.__handler = handler

    @property
    def args_(self):
        return self.__args

    @args_.setter
    def args_(self, args):
        self.__args = args

    @property
    def kwargs_(self):
        return self.__kwargs

    @kwargs_.setter
    def kwargs_(self, kwargs):
        self.__kwargs = kwargs
