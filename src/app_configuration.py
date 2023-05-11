class Config:
    SECRET_KEY = '0d99f6a17b6548608f5b408725edeec0jjiewu321oi54jos'
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    TESTING = True
    SECRET_KEY = '0d99f6a17b6548608f5b408725edeec0jjiewu321oi54jos'
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
