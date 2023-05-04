import pytest
from tests.fixtures import dummy_db, user_service

from src.service.user import UserService
from src.models import User, URL, Visit


def test_user_get(user_service: UserService):
    user = user_service.get_user(1)

    assert user.username == "Max"
    assert user.password == "max_123456"

    with pytest.raises(ValueError):
        user_service.get_user(6)


def test_user_get_all(user_service: UserService):
    assert len(user_service.get_all_users()) == 3


def test_user_create(user_service: UserService):
    amount_before = len(user_service.get_all_users())
    new_user = user_service.create_user("hello", "world")

    assert len(user_service.get_all_users()) - amount_before == 1
    assert new_user.username == "hello"
    assert new_user.check_password("world")


def test_user_update(user_service: UserService):
    user = user_service.get_user(1)
    user_upd = user_service.update_user(1, "new_pass")

    assert user.password == user_upd.password
    assert user.check_password("new_pass")


def test_user_delete(user_service: UserService):
    amount_before = len(user_service.get_all_users())
    user = user_service.delete_user(1)

    assert user.username == "Max"
    assert amount_before - len(user_service.get_all_users()) == 1
