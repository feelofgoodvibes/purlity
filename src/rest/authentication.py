from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, set_access_cookies
from src.service.user import UserService
from src.database import db

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True,
                    help='Username is required',
                    location="form")

parser.add_argument('password', type=str, required=True,
                    help='Password is required',
                    location="form")


class Registration(Resource):
    user_service = UserService(db)

    def post(self):
        args = parser.parse_args(req=request)

        username, password = args["username"], args["password"]

        try:
            user = self.user_service.create_user(username, password)
        except ValueError as e:
            return {"msg": str(e)}, 400

        db.session.commit()

        token = create_access_token(identity=user)
        return {"msg": "ok", "access_token": token}, 200


class Login(Resource):
    user_service = UserService(db)

    def post(self):
        args = parser.parse_args(req=request)

        username, password = args["username"], args["password"]

        user = self.user_service.get_user_by_username(username)
        
        if user is None:
            return {"msg": "User does not exist"}, 404
        
        if not user.check_password(password):
            return {"msg": "Wrong password"}, 400
        
        token = create_access_token(identity=user)

        response = jsonify({"access_token": token})
        set_access_cookies(response, token)

        return response
