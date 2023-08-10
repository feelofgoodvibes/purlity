from flask import render_template, make_response
from flask_jwt_extended import get_current_user, unset_jwt_cookies, jwt_required

@jwt_required(optional=True)
def login():
    current_user = get_current_user()
    response = make_response(render_template("login.html"), 200)

    if current_user is not None:
        unset_jwt_cookies(response)

    return response

@jwt_required(optional=True)
def register():
    current_user = get_current_user()
    response = make_response(render_template("register.html"), 200)

    if current_user is not None:
        unset_jwt_cookies(response)

    return response