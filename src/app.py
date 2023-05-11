from flask import Flask
from src.database import db, migrate
from src.rest import api_blueprint
from src.models import *
from src.jwt import jwt_manager


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_object("src.app_configuration.Config")
    else:
        app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app)
    jwt_manager.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
