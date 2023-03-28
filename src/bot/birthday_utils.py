from datetime import datetime, date

# from src.dao.dto import User

from loguru import logger


def _ru_age(age: int) -> str:
    if (age % 10 == 1) and (age != 11) and (age != 111):
        return "годик"
    elif (age % 10 > 1) and (age % 10 < 5) and (age != 12) and (age != 13) and (age != 14):
        return "годика"
    else:
        return "годиков"


def check_birthday(data: list[User], *, current_date: date | None = None) -> dict[int, list[User]]:
    now = current_date or datetime.now()
    nd, nm, ny = now.day, now.month, now.year
    today: dict[int, list[User]] = {}

    for d in data:
        chat_id = d.group_id
        if not d.birthday:
            logger.warning('No info about birthday for user: {}|{}, chat: {}'.format(d.tg_id, d.name, chat_id))
            continue
        dd, dm, dy = d.birthday.day, d.birthday.month, d.birthday.year
        if nm == dm:
            if nd == dd:
                logger.info('Today Birthday of user: {}|{}, chat: {}'.format(d.tg_id, d.name, chat_id))
                if chat_id not in today:
                    today[chat_id] = []
                today[chat_id].append(d)
            if 0 < dd - nd <= 7:
                logger.info('In {} days birthday of user: {}|{}, chat: {}'.format(dd - nd, d.tg_id, d.name, chat_id))
    return today


def create_birthday_message(birthdays: list[User]) -> str:
    text = """А кто это у нас хотел зашкериться? А? А? А?\nА я вам скажу кто ето, хе-хе-хе <i>фото_члена.jpg</i>\n"""
    if len(birthdays) > 1:
        user = ""
        for b in birthdays:
            age = b.how_many_years()
            user += "<i><b>{0:30s}</b></i> - <b>{1:4d}</b> {2}\n".format(b.name, age, _ru_age(age))
        text += "Так вот сегодня у нас несколько именинников:\n"
        text += user
        text += "Так восславим же этих бесславных котиков <b>выпивкой</b> и весельем, " \
                "что бы их душа попала в ВАЛЬГХАЛЛУ! (но не сегодня) \n"
    else:
        age = birthdays[0].how_many_years()
        text += "Так вот сегодня у нас день рождение у <i><b>{}</b></i>, и исполняется <b>{}</b> {}\n".format(
            birthdays[0].name, age, _ru_age(age)
        )
        text += "Так восславим же этого бесславного котика выпивкой и весельем, что бы его душа попала в ВАЛЬГХАЛЛУ! " \
                "(но не сегодня) \n"
    text += "<b><u>ДИСКЛЕЙМЕР</u></b>: <i>Употребление алкоголя приводит к " \
            "видосам которых вы потом будете стыдиться </i>"
    return text
