from typing import Union
from datetime import datetime, date, timezone
from dateutil import parser
from dateutil.tz import tzlocal


def to_datetime(value: Union[str, datetime, date]) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, date):
        dt = datetime.combine(value, datetime.min.time())
    else:
        dt = parser.parse(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tzlocal())
    return dt


def to_zulu_str(dt: datetime) -> str:
    dt_utc = dt.astimezone(timezone.utc)
    zulu_string = dt_utc.isoformat().replace('+00:00', 'Z')
    return zulu_string
