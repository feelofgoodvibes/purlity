import os
from datetime import datetime, timedelta
import orjson
import dotenv
from pydantic import BaseModel
from flask.json.provider import JSONProvider

dotenv.load_dotenv(dotenv.find_dotenv())

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)


class TestConfig:
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)


class OrJSONProvider(JSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        raise TypeError

    def dumps(self, obj, *, option=None, **kwargs):
        if option is None:
            option = orjson.OPT_APPEND_NEWLINE | orjson.OPT_PASSTHROUGH_DATETIME

        if isinstance(obj, BaseModel):
            obj = obj.dict()

        return orjson.dumps(obj, option=option, default=self.default).decode()

    def loads(self, s, **kwargs):
        return orjson.loads(s)
