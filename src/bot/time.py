import re
from datetime import datetime, timedelta, date


def seconds_first_start(start_time: str = '06:00') -> int:
    n = datetime.now()
    n = datetime.strptime('{}:{}:{}'.format(n.hour, n.minute, n.second), '%H:%M:%S')

    rt = datetime.strptime(start_time, '%H:%M')
    if n > rt:
        rt += timedelta(days=1)
    wt = rt - n
    return int(wt.total_seconds())


def to_datetime(dt: str | None) -> date | None:
    if dt is None:
        return None
    splitter = re.search(r'[./-]', dt).group()
    fmt = '%d{0}%m{0}%Y'.format(splitter)
    return datetime.strptime(dt, fmt).date()
