from flask import Flask
from src.database import db


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_object("src.app_configuration.Config")
    else:
        app.config.from_object(config)

    db.init_app(app)

    return app
