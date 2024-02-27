from apscheduler.triggers.cron import CronTrigger

from ego.scheduler.triggers.Trigger import Trigger


class AccurateCronTrigger(CronTrigger, Trigger):
    def __init__(self, **kwargs):
        super(AccurateCronTrigger, self).__init__(**kwargs)

    @classmethod
    def from_crontab(cls, expr, timezone=None):
        values = expr.split()
        length = len(values)
        if length == 5:
            return CronTrigger.from_crontab(expr, timezone)

        if len(values) != 7:
            raise ValueError(f"Wrong number of fields; got {len(values)}, expected 7")

        return cls(
            second=values[0],
            minute=values[1],
            hour=values[2],
            day=values[3],
            month=values[4],
            day_of_week=values[5],
            year=values[6],
            timezone=timezone
        )

    def from_date(self, *args, **kwargs):
        pass

    def from_datetime(self, *args, **kwargs):
        pass
