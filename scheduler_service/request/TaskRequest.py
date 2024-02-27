from ego.request.BaseParam import BaseParam


class TaskRequest(BaseParam):
    def __init__(self, body=None):
        self.__task_id = None
        self.__task_name = None
        self.__target = None
        self.__trigger = None
        self.__args = []
        self.__kwargs = {}
        self.__misfire_grace_time = -1
        self.__coalesce = False
        self.__max_instances = 1
        self.__next_run_time = None
        self.__executor = None
        self.__replace_existing = False

        self.mapping_body(body)

    @property
    def task_id(self):
        return self.__task_id

    @task_id.setter
    def task_id(self, task_id_):
        self.__task_id = task_id_

    @property
    def task_name(self):
        return self.__task_name

    @task_name.setter
    def task_name(self, task_name_):
        self.__task_name = task_name_

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target_):
        self.__target = target_

    @property
    def trigger(self):
        return self.__trigger

    @trigger.setter
    def trigger(self, trigger_):
        self.__trigger = trigger_

    @property
    def args(self):
        return self.__args

    @args.setter
    def args(self, args_):
        self.__args = args_

    @property
    def kwargs(self):
        return self.__kwargs

    @kwargs.setter
    def kwargs(self, kwargs_):
        self.__kwargs = kwargs_

    @property
    def misfire_grace_time(self):
        return self.__misfire_grace_time

    @misfire_grace_time.setter
    def misfire_grace_time(self, misfire_grace_time_):
        self.__misfire_grace_time = misfire_grace_time_

    @property
    def coalesce(self):
        return self.__coalesce

    @coalesce.setter
    def coalesce(self, coalesce_):
        self.__coalesce = coalesce_

    @property
    def max_instances(self):
        return self.__max_instances

    @max_instances.setter
    def max_instances(self, max_instances_):
        self.__max_instances = max_instances_

    @property
    def next_run_time(self):
        return self.__next_run_time

    @next_run_time.setter
    def next_run_time(self, next_run_time_):
        self.__next_run_time = next_run_time_

    @property
    def executor(self):
        return self.__executor

    @executor.setter
    def executor(self, executor_):
        self.__executor = executor_

    @property
    def replace_existing(self):
        return self.__replace_existing

    @replace_existing.setter
    def replace_existing(self, replace_existing_):
        self.__replace_existing = replace_existing_
