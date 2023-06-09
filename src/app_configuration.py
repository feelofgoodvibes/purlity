from flask.json.provider import JSONProvider
from pydantic import BaseModel
import orjson
from datetime import datetime


class Config:
    SECRET_KEY = '0d99f6a17b6548608f5b408725edeec0jjiewu321oi54jos'
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    TESTING = True
    SECRET_KEY = '0d99f6a17b6548608f5b408725edeec0jjiewu321oi54jos'
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
