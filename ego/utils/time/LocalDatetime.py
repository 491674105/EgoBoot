from calendar import monthrange

from datetime import datetime, timedelta
from time import time
from time import timezone

from ego.utils.number.Number import calc_number_digits


class LocalDatetime(datetime):
    @classmethod
    def instance_with_datetime(cls, dt):
        return super().__new__(
            cls, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo, fold=dt.fold
        )

    @classmethod
    def parse_datetime_string(cls, dt, fmt="%Y-%m-%d %H:%M:%S"):
        """
            datetime-string 转 LocalDatetime
        """
        return cls.instance_with_datetime(cls.strptime(dt, fmt))

    def datetime_format(self, fmt="%Y-%m-%d %H:%M:%S"):
        """
            格式化LocalDatetime
        """
        return self.strftime(fmt)

    @classmethod
    def get_time_of_second(cls, differ=0):
        """
            获取秒级时间戳
            注：存在线程安全问题，禁止用于自增主键生成
        """
        return int(time()) - differ

    @classmethod
    def get_time_of_ms(cls, differ=0):
        """
            获取毫秒级时间戳
            注：存在线程安全问题，禁止用于自增主键生成
        """
        return int(time() * 1000) - differ

    @classmethod
    def get_datetime_by_timestamp(cls, ts):
        """
            将10/13位时间戳转换为LocalDatetime
        """
        digits = calc_number_digits(ts)
        if digits == 10:
            return cls.fromtimestamp(ts)

        if digits == 13:
            return cls.fromtimestamp(ts / 1000.0)

    @classmethod
    def get_utc_datetime_by_timestamp(cls, ts):
        """
            将10/13位时间戳转换为UTC形式LocalDatetime
            %Y-%m-%dT%H:%M:%SZ
        """
        digits = calc_number_digits(ts)
        if digits == 10:
            return cls.utcfromtimestamp(ts)

        if digits == 13:
            return cls.utcfromtimestamp(ts / 1000.0)

    @classmethod
    def get_utc_datetime(cls, hours, dt=None):
        if not dt:
            tg_dt = cls.now()
        else:
            tg_dt = dt
        return tg_dt + timedelta(hours=hours)

    def get_utc_offset(self, radix=1):
        return timezone / radix

    def get_the_first_date_of_month(self):
        """
            获取指定日期对应月份的第一天
        """
        return self - timedelta(days=self.day - 1)

    def get_the_last_date_of_month(self):
        """
            获取指定日期对应月份的最后一天
        """
        return self.replace(day=monthrange(self.year, self.month)[1])

    def get_before_dawn(self):
        """
            获取凌晨零点
        """
        return self - timedelta(hours=self.hour, minutes=self.minute, seconds=self.second, microseconds=self.microsecond)

    def get_midnight(self):
        """
            获取午夜，一般为23:59:59
        """
        return self.get_before_dawn() + timedelta(hours=23, minutes=59, seconds=59)

    def plusYear(self, years: int):
        """
            向前调整年份
        """
        return self.replace(year=(self.year + years))

    def plusMonth(self, month: int):
        """
            向前调整月份
        """
        new_month = self.month + month
        if new_month <= 12:
            return self.replace(month=new_month)

        return self.replace(year=self.year + (new_month // 12), month=(new_month % 12))

    def plusDay(self, days: int):
        """
            向前调整天数
        """
        return self + timedelta(days=days)

    def plusHour(self, hours: int):
        """
            向前调整小时
        """
        return self + timedelta(hours=hours)

    def plusMinute(self, minutes: int):
        """
            向前调整分钟
        """
        return self + timedelta(minutes=minutes)

    def plusSecond(self, seconds: int):
        """
            向前调整秒
        """
        return self + timedelta(seconds=seconds)

    def minusYear(self, years: int):
        """
            向后调整年份
        """
        return self.replace(year=(self.year - years))

    def minusMonth(self, month: int):
        """
            向后调整月份
        """
        new_month = self.month - month
        if new_month == 0:
            return self.replace(year=(self.year - 1), month=12)

        if new_month > 0:
            return self.replace(month=new_month)

        if new_month > -12:
            return self.replace(year=(self.year - 1), month=(12 + new_month))

        return self.replace(year=(self.year + (new_month // 12) - 1), month=(12 + (new_month % 12)))

    def minusDay(self, days: int):
        """
            向后调整天
        """
        return self - timedelta(days=days)

    def minusHour(self, hours: int):
        """
            向后调整小时
        """
        return self - timedelta(hours=hours)

    def minusMinute(self, minutes: int):
        """
            向后调整分钟
        """
        return self - timedelta(minutes=minutes)

    def minusSecond(self, seconds: int):
        """
            向后调整秒
        """
        return self - timedelta(seconds=seconds)
