from flask import redirect, url_for
from flask_jwt_extended import JWTManager, unset_jwt_cookies
from src.database import db
from src.service.user import UserService

jwt_manager = JWTManager()
user_service = UserService(db)


@jwt_manager.user_identity_loader
def user_identity_loader(user):
    return user.id


@jwt_manager.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return user_service.get_user(identity)


@jwt_manager.expired_token_loader
def token_expired(_jwt_header, jwt_data):
    response = redirect(url_for("webapp.index"))
    unset_jwt_cookies(response)
    return response