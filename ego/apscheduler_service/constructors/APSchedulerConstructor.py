# Unix/Linux环境下有效
try:
    from fcntl import flock
    from fcntl import LOCK_EX, LOCK_NB, LOCK_UN

    lock_module_valid = True
except ModuleNotFoundError:
    lock_module_valid = False

from ego import applicationContext
from ego.logger.service.LoggerCoreService import LoggerCoreService
from ego.database_core.service.DatabaseCoreService import DatabaseCoreService
from ego.scheduler.constructors.Constructor import Constructor
from ego.apscheduler_service.schedulers.SingleBackgroundScheduler import SingleBackgroundScheduler

from ego.common.constant.config import Base

log = None


class APSchedulerConstructor(Constructor):
    @staticmethod
    def lock(file):
        if lock_module_valid:
            flock(file, LOCK_EX | LOCK_NB)

    @staticmethod
    def un_lock(file):
        if lock_module_valid:
            flock(file, LOCK_UN)

    @staticmethod
    def create_schedulers(sch_metas):
        if not sch_metas:
            return

        lock_file_path = getattr(applicationContext, Base.MODULE_PATH_KEY)
        lock_file = open(f"{lock_file_path}/aps_scheduler.lock", "wb")
        try:
            # 获取锁
            APSchedulerConstructor.lock(lock_file)
            start_flag = False
        except OSError:
            # 无法获取锁，认为有其他进程完成持锁
            start_flag = True

        # 创建全局任务调度容器
        for sch_meta in sch_metas:
            if start_flag:
                if "skip_start_check" not in sch_meta or not sch_meta["skip_start_check"]:
                    continue
                APSchedulerConstructor.create_scheduler(sch_meta)
                continue

            APSchedulerConstructor.create_scheduler(sch_meta)

        APSchedulerConstructor.un_lock(lock_file)
        lock_file.close()

    @staticmethod
    def create_scheduler(sch_meta):
        global log
        if not log:
            log = LoggerCoreService.get_logger_instance()

        if "table_name" not in sch_meta or sch_meta["table_name"] == "":
            scheduler = SingleBackgroundScheduler.create_scheduler_with_database(
                engine=None,
                timezone=sch_meta["timezone"],
                table_name=None
            )
        else:
            scheduler = SingleBackgroundScheduler.create_scheduler_with_database(
                engine=DatabaseCoreService.get_engine_instance(Base.ENGINE_KEY),
                timezone=sch_meta["timezone"],
                table_name=sch_meta["table_name"]
            )

        if hasattr(applicationContext, sch_meta["sch_name"]):
            log.debug(f"调度器[{sch_meta['sch_name']}]已启动。")
            return
        setattr(applicationContext, sch_meta["sch_name"], scheduler)
        scheduler.start()

    @staticmethod
    def constructor(base_config, *args, **kwargs):
        global log
        log = LoggerCoreService.get_logger_instance()

        scheduler_names = [
            # 全局系统调度器
            {
                "sch_name": "sys_scheduler",
                "timezone": base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["timezone"],
                "skip_start_check": True
            },
            # 全局业务调度器
            {
                "sch_name": "business_scheduler",
                "timezone": base_config[getattr(applicationContext, Base.BASE_CONFIG_VALID_KEY)]["timezone"],
                "table_name": f"{applicationContext.service_name}_service_bs_jobs"
            }
        ]
        APSchedulerConstructor.create_schedulers(scheduler_names)
