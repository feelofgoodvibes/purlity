from flask import Blueprint
from flask_restful import Api
from src.rest.authentication import Registration, Login


api_blueprint = Blueprint("api", __name__)

api = Api()
api.add_resource(Registration, "/register")
api.add_resource(Login, "/login")

api.init_app(api_blueprint)
