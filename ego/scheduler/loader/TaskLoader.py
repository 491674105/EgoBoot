from ego.classloader.base.BaseLoader import BaseLoader


class TaskLoader(BaseLoader):

    def __init__(self, base_load_path, *args, **kwargs):
        super().__init__(base_load_path, *args, **kwargs)

    def load_tasks(self):
        self.scanner()
        self.load()

    def scanner(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass

    def load_task_cls(self, clazz):
        pass

    def load_task_func(self, func, crontab):
        pass
