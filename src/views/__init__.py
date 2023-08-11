import os
from flask import Blueprint, render_template, flash
from src.views.authentication import login, register
from src.views.index import index
from flask_jwt_extended import get_current_user, jwt_required


templates_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'static')


webapp_blueprint = Blueprint("webapp",
                             __name__,
                             template_folder=templates_folder,
                             static_folder=static_folder)

webapp_blueprint.add_url_rule("/login", view_func=login)
webapp_blueprint.add_url_rule("/register", view_func=register)
webapp_blueprint.add_url_rule("/", view_func=index)