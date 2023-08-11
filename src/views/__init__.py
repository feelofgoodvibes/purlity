import os
from flask import Blueprint
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