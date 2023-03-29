import datetime
import json
import os.path
from pathlib import Path

import pytest

from src.bot.dto.user import User
from src.bot.functions.birthday_utils import check_birthday, create_birthday_message


@pytest.fixture
def users() -> list[User]:
    path = Path(os.path.dirname(__file__), 'fixtures', 'users.json')
    with open(path, 'r') as f:
        return [User(**u) for u in json.load(f)]


def test_check_birthday(users: list[User]):
    c = datetime.date(2022, 10, 22)
    result = check_birthday(users, current_date=c)
    assert result
    assert len(result) == 3
    assert len(result[111111]) == 76
    assert len(result[22222]) == 86
    assert len(result[33333]) == 65


def test_create_birthday_message(users: list[User]):
    u = users[666]
    result = create_birthday_message([u])
    assert result
    assert '<i><b>Maxim</b></i>, и исполняется <b>32</b>' in result
