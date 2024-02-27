class Shutdown:
    def __init__(self, *args, **kwargs):
        pass

    def register(self, signal_handlers=None):
        """
            注册停服事件
        """
        pass

    def _shutdown(self, sig_no, stack_frame):
        """
            停服处理函数
        """
        pass
