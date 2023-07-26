from flask import Blueprint
from flask_restful import Api
from src.rest.authentication import Registration, Login
from src.rest.url import URL
from src.rest.url_collection import URL_collection


api_blueprint = Blueprint("api", __name__)

api = Api()
api.add_resource(Registration, "/register")
api.add_resource(Login, "/login")
api.add_resource(URL_collection, '/url')
api.add_resource(URL, '/url/<string:short_url>')

api.init_app(api_blueprint)
