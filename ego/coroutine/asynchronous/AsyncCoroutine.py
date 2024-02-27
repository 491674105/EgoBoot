from threading import Thread

from asyncio import Future
from asyncio import new_event_loop, set_event_loop, ensure_future, sleep

from ego.coroutine.Coroutine import Coroutine


class AsyncCoroutine(Thread, Coroutine):
    def __init__(self, name=None, timeout=0, callback=None, *args, **kwargs):
        Thread.__init__(self)
        Coroutine.__init__(self)

        Thread.setName(self=self, name=name)

        self.timeout = timeout
        self.callback = callback

        self.args = args
        self.kwargs = kwargs

        self.loop = None
        self.future = None
        self.result = None

    def __exec_loop(self):
        self.__create_loop()

    def __create_loop(self):
        self.loop = new_event_loop()
        set_event_loop(self.loop)
        self.future = Future(loop=self.loop)
        ensure_future(self.__register_callbacks())
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

    async def __register_callbacks(self):
        await self.__wait()
        self.future.add_done_callback(self.__call_result)
        if self.callback:
            self.future.set_result(self.callback(*self.args, **self.kwargs))

    def __wait(self):
        if self.timeout > 0:
            return sleep(self.timeout)
        else:
            return self.future

    def __call_result(self, future):
        self.result = future.result()
        self.loop.stop()

    def run(self):
        self.__exec_loop()

    def stop(self):
        self.loop.stop()

    def close(self):
        self.loop.close()
