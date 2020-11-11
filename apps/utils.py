import arrow
from datetime import datetime


def to_arrow(in_datetime: datetime, tz: str = "America/Santiago") -> arrow.Arrow:
    return arrow.Arrow(
        year=in_datetime.year,
        month=in_datetime.month,
        day=in_datetime.day,
        hour=in_datetime.hour,
        minute=in_datetime.minute,
        second=in_datetime.second,
        tzinfo=tz
    )