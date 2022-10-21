import re
from datetime import datetime, timedelta, date

import pytz
from loguru import logger


def seconds_first_start(start_time: str = '00:01', timezone: pytz.BaseTzInfo | None = None) -> int:
    n = datetime.now(timezone)
    n = datetime.strptime('{}:{}:{}'.format(n.hour, n.minute, n.second), '%H:%M:%S')

    rt = datetime.strptime(start_time, '%H:%M')
    if n > rt:
        rt += timedelta(days=1)
    wt = rt - n
    logger.info("First run start: ~{0} h, now: {1}".format(wt.total_seconds()/3600, n.strftime('%H:%M:%S')))
    return int(wt.total_seconds())


def _to_datetime(dt: str | None) -> date | None:
    if dt is None:
        return None
    splitter = re.search(r'[./-]', dt).group()
    fmt = '%d{0}%m{0}%Y'.format(splitter)
    return datetime.strptime(dt, fmt).date()
