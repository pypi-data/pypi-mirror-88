from typing import TypeVar, Callable, Union
import datetime as dt
from enum import IntEnum, auto
from ..core import curry, when, is_a


__all__ = (
    'daterange',
    'format_dt',
    'fromtimestamp',
    'FreqName',
    'locnow',
    'localize',
    'now',
    'fmt_std_date',
    'fmt_std_datetime',
    'timestamp',
    'timestamp_ms',
    'to_datetime',
    'today',
    'utcnow',
)


AnyDateTime = TypeVar('AnyDateTime', dt.date, dt.datetime)

now: Callable[[], dt.datetime] = dt.datetime.now
utcnow: Callable[[], dt.datetime] = dt.datetime.utcnow
today = dt.date.today


def locnow():
    from dateutil.tz import tzlocal
    return now(tzlocal())


def timestamp(d: dt.datetime = None):
    return int(d.timestamp() if d else now().timestamp())


def timestamp_ms(d: dt.datetime = None):
    return int(d.timestamp() if d else now().timestamp()) * 1000


@curry
def localize(_tz: dt.tzinfo, t1: dt.datetime):
    return t1.astimezone(_tz)


def fromtimestamp(tmp):
    try:
        return dt.datetime.fromtimestamp(float(tmp))
    except (TypeError, ValueError):
        return None


def to_datetime(raw):
    from dateutil.parser import parse
    if is_a((str, bytes), raw) and raw.isdigit():
        raw = int(raw)
    try:
        return when([
            (is_a((str, bytes)), parse),
            (is_a((int, float)), fromtimestamp),
        ], None)(raw)
    except (ValueError, TypeError):
        return None


@curry
def format_dt(p: str, d: AnyDateTime):
    return d.strftime(p) if d else ''


fmt_std_date = format_dt('%Y-%m-%d')
fmt_std_datetime = format_dt('%Y-%m-%d %H:%M:%S')


class FreqName(IntEnum):
    Yearly = auto()
    Monthly = auto()
    Weekly = auto()
    Daily = auto()
    Hourly = auto()
    Minutely = auto()
    Secondly = auto()


@curry
def daterange(freq: Union[int, FreqName], start_date, **kwargs):
    """
    生产一个日期列表，使用dateutil.rrule
    :param freq: FreqName
        生成的频率：年(0)、月(1)、周(2)、日(3)、小时(4)、分(5)、秒(6)
    :param start_date: 开始日期
    :param kwargs:
        @see dateutil.rrule
    :return:
    """
    from dateutil.rrule import rrule
    value = freq.value - 1 if isinstance(freq, FreqName) else freq

    return rrule(value, dtstart=start_date, **kwargs)




