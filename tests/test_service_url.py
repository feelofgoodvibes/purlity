import pytest
from tests.fixtures import dummy_db, url_service
from src.models import User, URL, Visit
from src.service.url import URLService


def test_url_get(url_service: URLService):
    url = url_service.get_url("YouTb")

    assert url.url == "http://youtube.com"

    with pytest.raises(ValueError):
        url_service.get_url("RnDom")


def test_get_all_urls(url_service: URLService):
    assert len(url_service.get_all_urls()) == 5


def test_create_url(url_service: URLService, monkeypatch):
    chars = iter("aaaaaaaac")
    monkeypatch.setattr("src.service.url.choice", lambda _: next(chars))

    url = url_service.create_url(user_id=1, url="http://test.com")
    url_service.db.session.commit()

    assert url.short_url == "aaaa"
    assert url.url == "http://test.com"
    assert url.user.username == "Max"
    
    url = url_service.create_url(user_id=2, url="http://test2.com")
    url_service.db.session.commit()
    
    assert url.short_url == "aaaac"
    assert url.url == "http://test2.com"
    assert url.user.username == "Kevin"


def test_delete_url(url_service: URLService):
    url_service.delete_url("gitHB")
    url_service.db.session.commit()

    assert len(url_service.get_all_urls()) == 4
    assert len(Visit.query.all()) == 14