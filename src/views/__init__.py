import os
from flask import Blueprint
from flask_jwt_extended import get_jwt, get_current_user, create_access_token, set_access_cookies
from datetime import datetime, timezone, timedelta
from src.views.authentication import login, register
from src.views.index import index
from src.views.url import view_short_url, goto_url


templates_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'static')


webapp_blueprint = Blueprint("webapp",
                             __name__,
                             template_folder=templates_folder,
                             static_folder=static_folder)

webapp_blueprint.add_url_rule("/login", view_func=login)
webapp_blueprint.add_url_rule("/register", view_func=register)
webapp_blueprint.add_url_rule("/", view_func=index)
webapp_blueprint.add_url_rule("/v/<string:short_url>", view_func=goto_url)
webapp_blueprint.add_url_rule("/<string:short_url>", view_func=view_short_url)


@webapp_blueprint.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_current_user())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response
