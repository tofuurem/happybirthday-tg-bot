from datetime import datetime, date

from loguru import logger

from src.dao.dto.database import User


def check_birthday(data: list[User], *, current_date: date | None = None) -> list[User]:
    now = current_date or datetime.now()
    nd, nm, ny = now.day, now.month, now.year
    today: list[User] = []

    for d in data:
        dd, dm, dy = d.birthday.day, d.birthday.month, d.birthday.year
        if nm == dm:
            if nd == dd:
                logger.info('Today Birthday of user: {}|{}'.format(d.tg_id, d.name))
                today.append(d)
            if 0 < dd - nd <= 7:
                logger.info('In {} days birthday of user: {}|{}'.format(dd - nd, d.tg_id, d.name))
    return today
