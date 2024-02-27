from abc import ABCMeta
from abc import abstractmethod


class Scheduler:
    """
        调度器抽象
        注：不同的框架会有不同的实现，需要具体参考引用的调度框架的规则
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(self, *args, **kwargs):
        """
            注册逻辑相关
        """
        pass

    @abstractmethod
    def unregister(self, *args, **kwargs):
        """
            注销逻辑相关
        """
        pass

    @abstractmethod
    def start(self, *args, **kwargs):
        """
            启动调度器
        """
        pass

    @abstractmethod
    def shutdown(self, *args, **kwargs):
        """
            停止调度器
        """
        pass

    @abstractmethod
    def query_job(self, *args, **kwargs):
        """
            查询任务
        """
        pass

    @abstractmethod
    def add_job(
        self,
        id,
        name,
        trigger,
        target=None,
        func=None,
        args=[],
        kwargs={},
        misfire_grace_time=-1,
        coalesce=False,
        max_instances=1,
        executor=None,
        replace_existing=False,
        *e_args,
        **e_kwargs
    ):
        """
            新建任务
            id：指定作业的唯一ID
            name：指定作业的名字
            func：Job执行的函数
            trigger：触发器，用于确定Job的执行时间。(str或trigger对象)
                根据设置的trigger规则，计算得到下次执行此job的时间， 满足时将会执行。
                date: 指定某个时间点出发，只执行一次
                    调用方式：
                        trigger="date"
                        定时方式一：run_date=datetime(1970, 1, 1, 8, 0, 0)
                        定时方式二：run_date="1970-01-01 08:00:00"
                cron: 可以指定时间、时间间隔、时间范围等
                    调用方式：
                        1. trigger="cron"
                            kwargs中传入对应日期时间参数
                        2. from ego.apscheduler_service.triggers.AccurateCronTrigger import AccurateCronTrigger
                            trigger=AccurateCronTrigger.from_crontab([crontab_condition_str])
                interval: 指定时间间隔出发任务，可指定时间范围
                    调用方式：
                        trigger="interval"
                        kwargs中传入对应日期时间参数
            args：Job执行函数需要的位置参数
            kwargs：Job执行函数需要的关键字参数
                trigger="date"    （只在给定的时间运行一次）
                    主要kwargs参数
                        run_date：datetime|str，指定运行时间。
                        timezone：datetime.tzinfo|str
                trigger="cron"
                    主要kwargs参数
                        year：int/str，4位
                        month：int/str，[1, 12]
                        day：int/str，[1, 31]
                        week：int/str，[1, 53]
                        day_of_week：int/str，[0, 6]，从周一开始，也可以用英文的钱三个小写字母。
                        hour：int/str，[0, 23]
                        minute：int/str，[0, 59]
                        second：int/str，[0, 59]
                        start_date：datetime/str
                        end_date：datetime/str
                        timezone：datetime.tzinfo|str
                        jitter：int/None，运行时间随机偏移[-jitter, jitter]秒
                    对于没有指定的参数，根据输入参数分别设置为*或最小值
                        大于指定元素中最小的，设置为 *
                        小于指定元素中最小的，设置为其最小值。
                        举例：输入 day=1, minute=20，则设置second=0，其他元素为*
                trigger="interval"
                    主要kwargs参数
                        weeks：int
                        days：int
                        hours：int
                        minutes：int
                        seconds：int
                        start_date：datetime/str
                        end_date：datetime/str
                        timezone：datetime.tzinfo|str
                        jitter：int/None，运行时间随机偏移[-jitter, jitter]秒
            misfire_grace_time：Job的延迟执行时间
                例如Job的计划执行时间是21:00:00，但因服务重启或其他原因导致21:00:31才执行，
                    如果设置此key为40, 则该job会继续执行，否则将会丢弃此job。
            coalesce：Job是否合并执行，是一个bool值。
                例如scheduler停止20s后重启启动，而job的触发器设置为5s执行一次，因此此job错过了4个执行时间，
                    如果设置为是，则会合并到一次执行，否则会逐个执行。
            max_instances：执行此job的最大实例数。
                executor执行job时，根据job的id来计算执行次数，根据设置的最大实例数来确定是否可执行。
            next_run_time：Job下次的执行时间。
                创建Job时可以指定一个时间[datetime]，不指定的话则默认根据trigger获取触发时间。
            executor：apscheduler定义的执行器。
                job创建时设置执行器的名字，根据字符串你名字到scheduler获取到执行此job的 执行器，执行job指定的函数。
            replace_existing: 布尔值，避免出现重复多个任务。默认False，server建议开启
        """
        pass

    @abstractmethod
    def add_jobs(self, *args, **kwargs):
        """
            批量新建任务
        """
        pass

    @abstractmethod
    def remove_job(self, *args, **kwargs):
        """
            删除任务
        """
        pass

    @abstractmethod
    def remove_jobs(self, *args, **kwargs):
        """
            批量删除任务
        """
        pass

    @abstractmethod
    def pause_job(self, *args, **kwargs):
        """
            暂停任务
        """
        pass

    @abstractmethod
    def resume_job(self, *args, **kwargs):
        """
            恢复被暂停的任务
        """
        pass

    @abstractmethod
    def modify_job(self, *args, **kwargs):
        """
            修改任务信息
        """
        pass

    @abstractmethod
    def reschedule_job(self, *args, **kwargs):
        """
            重新调度任务
        """
        pass
