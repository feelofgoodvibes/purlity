import pytest
from tests.fixtures import test_app, dummy_db, url_service

from src.models import User, URL, Visit
from src.service.url import URLService
from src.schemas.url import URLFilters


def test_url_get(url_service: URLService):
    url = url_service.get_url("YouTb")

    assert url.url == "http://youtube.com"

    with pytest.raises(ValueError):
        url_service.get_url("RnDom")


def test_get_all_urls(url_service: URLService):
    all_urls = url_service.get_all_urls()
    assert len(all_urls) == 5

    test_filters = [
        URLFilters.parse_obj({ "user": "1" }),
        URLFilters.parse_obj({ "date_from": "2023-05-02 13:00" }),
        URLFilters.parse_obj({ "date_from": "2023-05-02 12:00", "date_to": "2023-05-03 23:00" }),
        URLFilters.parse_obj({ "limit": 2, "offset": 1 }),
        URLFilters.parse_obj({ "user": 2, "limit": 1 }),
        URLFilters.parse_obj({ "user": 1, "offset": 1 }),
    ]

    expected_output = [
        [all_urls[0], all_urls[1]],
        [all_urls[2], all_urls[3], all_urls[4]],
        [all_urls[1], all_urls[2], all_urls[3]],
        [all_urls[1], all_urls[2]],
        [all_urls[2]],
        [all_urls[1]]
    ]

    for i, filters in enumerate(test_filters):
        assert url_service.get_all_urls(filters) == expected_output[i]


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

    with pytest.raises(ValueError):
        url_service.create_url(user_id=2, url="ttps://t.com")
        url_service.create_url(user_id=2, url="testfailure")


def test_delete_url(url_service: URLService):
    url_service.delete_url("gitHB")
    url_service.db.session.commit()

    assert len(url_service.get_all_urls()) == 4
    assert len(Visit.query.all()) == 14