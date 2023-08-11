from flask import Blueprint
from flask_restful import Api
from src.rest.authentication import Registration, Login, Logout
from src.rest.url import URL
from src.rest.url_collection import URL_collection


api_blueprint = Blueprint("api", __name__)

api = Api()
api.add_resource(Registration, "/register", endpoint='register')
api.add_resource(Login, "/login", endpoint='login')
api.add_resource(Logout, "/logout", endpoint='logout')
api.add_resource(URL_collection, '/url', endpoint='urls')
api.add_resource(URL, '/url/<string:short_url>')

api.init_app(api_blueprint)
