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

    def __str__(self) -> str:
        return f"""
        {self.name:20s} | <i>{self.birthday.strftime('%d.%m.%Y') if self.birthday else 'No info about birthday':20s} </i>
        """
