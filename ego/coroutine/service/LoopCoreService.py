from ego import applicationContext
from ego.exception.type.NullPointException import NullPointException


class LoopCoreService:

    @staticmethod
    def get_loop_instance(key=None):
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not key or key == "":
            loop_name = "loop"
        else:
            loop_name = key

        return getattr(applicationContext, loop_name)

    @staticmethod
    def get_loop_thread(key=None):
        if not applicationContext:
            raise NullPointException("ApplicationContext is empty.")

        if not key or key == "":
            loop_thread_name = "loop_thread"
        else:
            loop_thread_name = key

        if not hasattr(applicationContext, loop_thread_name):
            raise NullPointException("No matching instances found.")

        return getattr(applicationContext, loop_thread_name)
