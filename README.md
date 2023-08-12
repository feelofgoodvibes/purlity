# 🔗 PURLITY
[![Building](https://github.com/feelofgoodvibes/purlity/actions/workflows/building.yml/badge.svg)](https://github.com/feelofgoodvibes/purlity/actions/workflows/building.yml)
[![Coverage Status](https://coveralls.io/repos/github/feelofgoodvibes/purlity/badge.svg)](https://coveralls.io/github/feelofgoodvibes/purlity)

![image](https://github.com/feelofgoodvibes/purlity/assets/53279267/f9abcb44-f8e4-43ba-82ae-0bde14b15aff)

PURLITY is a link shortener (also known as a URL shortener) service that takes a long URL and makes it shorter.
PURLITY provides:
* REST API for using the service
* Account system that is built using [JSON Web Tokens](https://jwt.io/)
* Possibility to make any URL shorter
* Statistics on visits of short url you've created

---

## Used technologies
#### Main
- [Flask](https://flask.palletsprojects.com) as web framework
- [SQLite](https://www.sqlite.org/index.html) as database
- [SQLAlchemy](https://www.sqlalchemy.org) + [Alembic](https://alembic.sqlalchemy.org) as ORM and migrations management
- [JSON Web Tokens](https://jwt.io/) for managing users accounts and REST API permissions

#### Additional
- [pytest](https://docs.pytest.org) as framework for testing
- [GitHub Actions](https://github.com/features/actions) as CI/CD
- [Coveralls.io](https://coveralls.io) + [Coverage](https://coverage.readthedocs.io/en/7.2.1/) as code coverage tracker

## REST API Endpoints

There is endpoints that requires `access_token` in the header or cookies of the request.

| Endpoint | Method | Description |
| - | - | - |
| **Account management** |   |   |
| `/api/register` | `POST` | Create a new account. Returns access_token of newly created user |
| `/api/login` | `POST` | Login to account. Returns access_token of user as JSON. Also, sets HTTP-only cookie. |
| `/api/logout` | `POST` | Logout from account. Unsets HTTP-only access_token cookie |
| **URL management** |  |  |
| `/api/url` | `GET` | Get list of urls created by user. Each URL has list of visits. Requires user access_token. Also, supports filtering.
|   | `POST` | Create new short url by passing link in body of the request |
| `/api/url/<short_url>` | `GET` | Get information about particular short url. If request made with access_token, returns list of visits too. |
|   | `DELETE` | Deletes short url|

## How to build & run
Before building, make sure you have python>=3.9 installed and configured. Also, It is recommended to build inside separate virtual environment:

1. Clone repository (`git clone https://github.com/feelofgoodvibes/purlity`)
2. Install dependencies (`pip install -r requirements.txt`)
3. Create `.env` file, and define `SECRET_KEY='your-secret-key'` there
4. Apply migrations to database:
  `flask --app src.app db upgrade`
5. Run application using `python run.py`

🎉 App is up and running (by default http://localhost:5000)
