from flask import Flask

from src.app_configuration import OrJSONProvider
from src.database import db, migrate

from src.models import *
from src.jwt import jwt_manager
from src.rest import api_blueprint
from src.views import webapp_blueprint


def create_app(config=None):
    app = Flask(__name__)
    app.json = OrJSONProvider(app)

    if config is None:
        app.config.from_object("src.app_configuration.Config")
    else:
        app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app)
    jwt_manager.init_app(app)

    app.register_blueprint(webapp_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
