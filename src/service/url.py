from random import choice
from string import ascii_letters
from typing import Optional
import validators

from src.models import URL
from src.database import SQLAlchemy
from src.service.user import UserService
from src.schemas.url import URLFilters


class URLService():
    """This class provides methods for managing short URLs."""
    
    URL_HASH_SYMBOLS = ascii_letters
    MIN_SHORT_URL_LENGTH = 4

    def __init__(self, db: SQLAlchemy):
        """
        Initialize the URLService with a SQLAlchemy instance.

        Args:
            db (SQLAlchemy): An instance of the SQLAlchemy database connection.
        """

        self.db = db
        self.user_service = UserService(db)

    def generate_short_url(self) -> str:
        """
        Generate a random short URL using URL_HASH_SYMBOLS.

        Returns:
            str: Randomly generated short URL.
        """

        short_url = "".join([choice(self.URL_HASH_SYMBOLS) for _ in range(self.MIN_SHORT_URL_LENGTH)])

        while True:
            try:
                self.get_url(short_url)
                short_url += choice(self.URL_HASH_SYMBOLS)
            except ValueError:
                break

        return short_url

    def get_all_urls(self, filters: Optional[URLFilters] = None) -> list[URL]:
        """
        Retrieve a list of URLs based on optional filters.

        Args:
            filters (URLFilters): URLFilters instance containing filter options. If `None`, all urls will be returned.

        Returns:
            list: List of URL objects matching the provided filters.
        """

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
        """
        Retrieve the URL by short URL.

        Args:
            short_url (str): Short URL to retrieve.

        Returns:
            URL: The URL object associated with the provided short URL.

        Raises:
            ValueError: If the URL is not found.
        """

        url = URL.query.filter(URL.short_url==short_url).first()

        if url is None:
            raise ValueError(f"URL-{short_url} not found!")

        return url

    def create_url(self, user_id: Optional[int], url: str) -> URL:
        """
        Create a new URL entry with a short URL, user ID, and original URL.

        Args:
            user_id (Optional[int]): User ID associated with the URL. Defaults to None.
            url (str): URL that needs to be shortened.

        Returns:
            URL: The newly created URL object.

        Raises:
            ValueError: If URL validation fails.
        """

        # Validating provided URL
        url_validate = validators.url(url)

        if not url_validate:
            raise ValueError("URL validation failed. Check if your URL is correct.")

        # Generating short url
        short_url = self.generate_short_url()

        new_url = URL(short_url=short_url, user_id=user_id, url=url)
        self.db.session.add(new_url)

        return new_url

    def delete_url(self, short_url: str) -> URL:
        """
        Delete the URL by short URL.

        Args:
            short_url (str): Short URL to be deleted.

        Returns:
            URL: The URL object that was deleted.

        Raises:
            ValueError: If the URL is not found.
        """

        url = self.get_url(short_url)
        self.db.session.delete(url)

        return url
