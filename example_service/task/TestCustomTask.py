from ego import applicationContext

log = applicationContext.log


class TestCustomTask:
    """
        自定义调度计划（测试）
        调度计划入口必须放置在最简洁的文件内，不能有过多过复杂的包引入，否则可能会导致文件无法解码引起调度任务元数据存储失败
    """

    def test_run_date(self, arg):
        log.debug("test_run_date")
        log.debug(arg)

    def test_run_date_no_args(self):
        log.debug("test_run_date_no_args")


def test_run_date_static(arg):
    log.debug("test_run_date")
    log.debug(arg)


def test_run_date_static_no_args():
    log.debug("test_run_date_static_no_args")
