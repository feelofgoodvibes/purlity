from random import choice
from string import ascii_letters
from typing import Optional

from src.models import URL
from src.database import SQLAlchemy
from src.service.user import UserService
from src.schemas import URLFilters


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

    def get_all_urls(self, filters: Optional[URLFilters] = None):
        query = URL.query

        if filters is not None:    
            if filters.user:
                query = query.filter(URL.user_id == filters.user)

            if filters.date_from:
                query = query.filter(URL.created_date >= filters.date_from)
            
            if filters.date_to:
                query = query.filter(URL.created_date <= filters.date_to)
            
            if filters.offset:
                query = query.offset(filters.offset)

            if filters.limit:
                query = query.limit(filters.limit)

        return query.all()

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
