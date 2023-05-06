from datetime import datetime
import pytest

from src.app import create_app, db
from src.models import User, URL, Visit
from src.service.user import UserService
from src.service.url import URLService
from src.service.visit import VisitService


@pytest.fixture()
def dummy_db():
    app = create_app("src.app_configuration.TestConfig")
    
    with app.app_context():
        # Create all tables
        db.create_all()

        # Populating User table
        db.session.add(User(username="Max", password="max_123456"))
        db.session.add(User(username="Kevin", password="applecider"))
        db.session.add(User(username="Jane", password="lovelylovely"))
        db.session.commit()

        # Populating URL table
        db.session.add(URL(user_id=1, url="http://example.com", short_url="exMpL", created_date=datetime(2023, 5, 1, 16, 0, 0)))
        db.session.add(URL(user_id=1, url="http://youtube.com", short_url="YouTb", created_date=datetime(2023, 5, 2, 12, 10, 0)))
        db.session.add(URL(user_id=2, url="http://github.com", short_url="gitHB", created_date=datetime(2023, 5, 2, 22, 0, 0)))
        db.session.add(URL(user_id=3, url="http://testing.com", short_url="tStin", created_date=datetime(2023, 5, 3, 12, 0, 0)))
        db.session.add(URL(user_id=3, url="http://python.org", short_url="pyThN", created_date=datetime(2023, 5, 5, 9, 0, 0)))
        db.session.commit()

        # Populating Visit table
        db.session.add(Visit(short_url="exMpL", date=datetime(2023, 5, 1, 16, 30, 00)))
        db.session.add(Visit(short_url="exMpL", date=datetime(2023, 5, 1, 22, 12, 00)))
        db.session.add(Visit(short_url="exMpL", date=datetime(2023, 5, 2, 3, 24, 00)))
        db.session.add(Visit(short_url="exMpL", date=datetime(2023, 5, 3, 11, 25, 00)))

        db.session.add(Visit(short_url="YouTb", date=datetime(2023, 5, 2, 10, 00, 00)))
        db.session.add(Visit(short_url="YouTb", date=datetime(2023, 5, 2, 12, 00, 00)))
        db.session.add(Visit(short_url="YouTb", date=datetime(2023, 5, 3, 13, 00, 00)))

        db.session.add(Visit(short_url="gitHB", date=datetime(2023, 5, 3, 1, 00, 00)))
        db.session.add(Visit(short_url="gitHB", date=datetime(2023, 5, 3, 21, 00, 00)))

        db.session.add(Visit(short_url="tStin", date=datetime(2023, 5, 3, 13, 25, 00)))
        db.session.add(Visit(short_url="tStin", date=datetime(2023, 5, 4, 8, 00, 00)))

        db.session.add(Visit(short_url="pyThN", date=datetime(2023, 5, 5, 10, 00, 00)))
        db.session.add(Visit(short_url="pyThN", date=datetime(2023, 5, 5, 11, 00, 00)))
        db.session.add(Visit(short_url="pyThN", date=datetime(2023, 5, 5, 16, 00, 00)))
        db.session.add(Visit(short_url="pyThN", date=datetime(2023, 5, 6, 8, 00, 00)))
        db.session.add(Visit(short_url="pyThN", date=datetime(2023, 5, 6, 15, 00, 00)))

        db.session.commit()

        yield db        # Returning db object

        db.drop_all()   # Dropping all tables after object used


@pytest.fixture()
def user_service(dummy_db) -> UserService:
    service = UserService(dummy_db)
    yield service


@pytest.fixture()
def url_service(dummy_db) -> URLService:
    service = URLService(dummy_db)
    yield service


@pytest.fixture()
def visit_service(dummy_db) -> VisitService:
    service = VisitService(dummy_db)
    yield service