from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from src.service.user import UserService
from src.database import db

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username is required', location="form")
parser.add_argument('password', type=str, required=True, help='Password is required', location="form")


class Registration(Resource):
    user_service = UserService(db)

    def post(self):
        args = parser.parse_args(req=request)

        username, password = args["username"], args["password"]

        try:
            user = self.user_service.create_user(username, password)
        except ValueError as e:
            return {"message": str(e)}

        db.session.commit()
        
        token = create_access_token(identity=user.id)
        return {"message": "ok", "access_token": token}


class Login(Resource):
    user_service = UserService(db)

    def post(self):
        args = parser.parse_args(req=request)

        username, password = args["username"], args["password"]

        user = self.user_service.get_user_by_username(username)
        
        if user is None:
            return {"message": "User does not exist"}
        
        if not user.check_password(password):
            return {"message": "Wrong password"}
        
        token = create_access_token(identity=user.id)

        return {"access_token": token}
