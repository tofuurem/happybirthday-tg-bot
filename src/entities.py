from datetime import date, datetime

from pydantic.main import BaseModel


class User(BaseModel):
    tg_id: int
    group_id: int | None
    name: str | None
    birthday: date | None
    # ToDo: create validation for date

    def how_many_years(self) -> int:
        return datetime.now().year - self.birthday.year

    def rkey(self) -> str:
        """
        Create redis key {tg_id}_{group_id)

        :return:
        """
        return "{}_{}".format(self.tg_id, self.group_id)

    def __str__(self) -> str:
        d = f"{self.birthday.strftime('%d.%m.%Y') if self.birthday else 'No info about birthday':20s}"
        return "{0:25s}|<i>{1:10s}</i>".format(self.name, d)
