from random import choice
from src.models import URL, User
from src.database import SQLAlchemy
from src.service.user import UserService
from typing import Union
from string import ascii_letters


class URLService():
    URL_HASH_SYMBOLS = ascii_letters
    MIN_SHORT_URL_LENGTH = 4

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.user_service = UserService(db)

    def generate_short_url(self) -> str:
        short_url = "".join([choice(self.URL_HASH_SYMBOLS) for _ in range(self.MIN_SHORT_URL_LENGTH)])

        while True:
            try:
                self.get_url(short_url)
                short_url += choice(self.URL_HASH_SYMBOLS)
            except ValueError:
                break

        return short_url

    def get_all_urls(self):
        return URL.query.all()

    def get_url(self, short_url: str) -> URL:
        url = URL.query.filter(URL.short_url==short_url).first()

        if url is None:
            raise ValueError(f"URL-{short_url} not found!")

        return url

    def create_url(self, user_id: int, url: str) -> URL:
        short_url = self.generate_short_url()

        new_url = URL(short_url=short_url, user_id=user_id, url=url)
        self.db.session.add(new_url)

        return new_url

    def delete_url(self, short_url: str) -> URL:
        url = self.get_url(short_url)
        self.db.session.delete(url)

        return url

