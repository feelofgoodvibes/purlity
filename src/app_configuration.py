class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
