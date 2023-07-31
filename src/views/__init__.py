import os
from flask import Blueprint, render_template, flash
from src.views.authentication import login, register
from flask_jwt_extended import get_current_user, jwt_required


templates_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'templates')
static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'static')


webapp_blueprint = Blueprint("webapp",
                             __name__,
                             template_folder=templates_folder,
                             static_folder=static_folder)

webapp_blueprint.add_url_rule("/login", view_func=login)
webapp_blueprint.add_url_rule("/register", view_func=register)

@webapp_blueprint.route("/")
@jwt_required(optional=True)
def index():
    flash('test')
    user = get_current_user()
    return render_template("index.html", user=user)
