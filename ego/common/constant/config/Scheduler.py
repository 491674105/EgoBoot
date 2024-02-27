"""
    scheduler
"""
SCHEDULER_INIT_FLAG = "scheduler_init_flag"
WAIT_SCHEDULER_LOADED = "wait_scheduler_loaded"
SCHEDULER_CONFIG_KEY = "scheduler"
VALID_SCHEDULER_TYPE = "valid_scheduler_type"
DEFAULT_SCHEDULER_TYPE = "inline"
DEFAULT_INLINE_SCHEDULER_CLASS = "apscheduler"
DEFAULT_INLINE_SCHEDULER_PACKAGE = "ego.apscheduler_service.constructors.APSchedulerConstructor"
DEFAULT_INLINE_TASKLOADER_PACKAGE = "ego.apscheduler_service.loader.APSchedulerTaskLoader"
SCHEDULER_SERIVCE_NAME = {
    "key": "serivce_name",
    "default": "",
    "type": "string",
    "require": False,
    "description": ""
}
REPORTING_INTERVAL = {
    "key": "reporting_interval",
    "default": 5,
    "type": "int",
    "require": False,
    "description": ""
}
SCHEDULER_TYPE = {
    "key": "type",
    "default": DEFAULT_SCHEDULER_TYPE,
    "type": "string",
    "require": False,
    "description": ""
}
SCHEDULER_CLASS = {
    "key": "class",
    "default": DEFAULT_INLINE_SCHEDULER_CLASS,
    "type": "string",
    "require": False,
    "description": ""
}
SCHEDULER_PACKAGE = {
    "key": "package",
    "default": DEFAULT_INLINE_SCHEDULER_PACKAGE,
    "type": "string",
    "require": False,
    "description": ""
}
SCHEDULER_TASK_LOADER = {
    "key": "task_loader",
    "default": DEFAULT_INLINE_TASKLOADER_PACKAGE,
    "type": "string",
    "require": False,
    "description": ""
}

SCHEDULER_WORKER_CLASS = {
    DEFAULT_INLINE_SCHEDULER_CLASS: DEFAULT_INLINE_SCHEDULER_PACKAGE,
    "airflow": "",
    "celery": "",
    "outline": "ego.scheduler_service.constructors.SchedulerServiceConstructor"
}
