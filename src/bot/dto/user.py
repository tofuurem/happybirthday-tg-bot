
class User(BaseModel):
    tg_id: int
    group_id: int | None
    name: str | None
    birthday: date | None
    sex: Literal["М", "Ж"] | None = None

    def how_many_years(self) -> int:
        return datetime.now().year - self.birthday.year

    def __str__(self) -> str:
        d = f"{self.birthday.strftime('%d.%m.%Y') if self.birthday else 'No info about birthday':20s}"
        sex = "({0:1s}) ".format(self.sex) if self.sex is not None else ''
        return "{1}{0:25s} | <i>{2:10s}</i>".format(self.name, sex, d)
