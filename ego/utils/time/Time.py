from enum import Enum, unique

from calendar import monthrange
from datetime import datetime, timedelta
from time import time
from time import timezone

from ego.utils.number.Number import calc_number_digits


@unique
class TimeChangeMethod(Enum):
    FORWARD = 1
    BACK = 0


@unique
class PeriodType(Enum):
    YEAR = 0
    MONTH = 1
    DAYOFMONTH = 2
    HOUR = 3
    MINUTE = 4
    SECOND = 5
    MICROSECOND = 6


def get_time_of_second(differ=0):
    """
        获取秒级时间戳
        注：存在线程安全问题，禁止用于自增主键生成
    """
    return int(time()) - differ


def get_time_of_ms(differ=0):
    """
        获取毫秒级时间戳
        注：存在线程安全问题，禁止用于自增主键生成
    """
    return int(time() * 1000) - differ


def get_datetime_by_timestamp(ts):
    """
        将10/13位时间戳转换为datetime
    """
    digits = calc_number_digits(ts)
    if digits == 10:
        return datetime.fromtimestamp(ts)

    if digits == 13:
        return datetime.fromtimestamp(ts / 1000.0)


def get_utc_datetime_by_timestamp(ts):
    """
        将10/13位时间戳转换为UTC形式datetime
        %Y-%m-%dT%H:%M:%SZ
    """
    digits = calc_number_digits(ts)
    if digits == 10:
        return datetime.utcfromtimestamp(ts)

    if digits == 13:
        return datetime.utcfromtimestamp(ts / 1000.0)


def get_datetime():
    return datetime.now()


def get_utc_datetime(hours, dt=None):
    if not dt:
        tg_dt = get_datetime()
    else:
        tg_dt = dt
    return tg_dt + timedelta(hours=hours)


def get_utc_offset(radix=1):
    return timezone / radix


def datetime_format(dt, fmt="%Y-%m-%d %H:%M:%S"):
    """
        格式化datetime
    """
    return dt.strftime(fmt)


def parse_datetime_string(dt, fmt="%Y-%m-%d %H:%M:%S"):
    """
        datetime-string 转 datetime
    """
    return datetime.strptime(dt, fmt)


def get_datetime_with_timedelta(cm=TimeChangeMethod.FORWARD, now=None, years=0, months=0, **kwargs):
    """
        通过指定时间间隔获取日期时间
        years：年间隔
        months：月间隔
        weeks：周间隔
        days：日间隔
        hours：小时间隔
        minutes：分间隔
        seconds：秒间隔
        milliseconds：毫秒间隔
        microseconds：微秒间隔
    """
    if now is None:
        now = datetime.now()

    if cm == TimeChangeMethod.BACK:
        if years > 0:
            now = now.replace(year=(now.year - years))
        if months > 0:
            now = now.replace(month=(now.month - months))
        if not kwargs:
            return now

        return now - timedelta(**kwargs)

    if years > 0:
        now = now.replace(year=(now.year + years))
    if months > 0:
        now = now.replace(month=(now.month + months))
    if not kwargs:
        return now
    return now + timedelta(**kwargs)


def get_the_first_date_of_month(dt: datetime):
    """
        获取指定日期对应月份的第一天
    """
    first = dt - timedelta(days=dt.day - 1)

    return first


def get_the_last_date_of_month(dt: datetime):
    """
        获取指定日期对应月份的最后一天
    """
    return dt.replace(day=monthrange(dt.year, dt.month)[1])
