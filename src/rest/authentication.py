from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
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
    """
    Registration Resource
    
    Provides an endpoint for user registration.

    Methods:
        `post(self)`
            Handles POST requests for user registration.
    """

    user_service = UserService(db)

    def post(self):
        """
        Handles user registration.
        
        This endpoint expects arguments as form data:
            * username (str, max 32 characters)
            * password (str, max 32 characters)

        Returns HTTP codes and data:
            200 return code, access_token - If user registration successful
            400 return code, error msg - If password is incorrect or username, login is more than 32 characters
        """

        args = parser.parse_args(req=request)

        username, password = args["username"], args["password"]

        # Validation
        if len(username) > 32 or len(password) > 32:
            return {"msg": "Username or password too long (max 32 characters)"}, 400

        try:
            user = self.user_service.create_user(username, password)
        except ValueError as e:
            return {"msg": str(e)}, 400

        db.session.commit()

        token = create_access_token(identity=user)
        return {"msg": "ok", "access_token": token}, 200


class Login(Resource):
    """
    Login Resource
    
    Provides an endpoint for user login.

    Methods:
        `post(self)`
            Handles POST requests for user login.
    """

    user_service = UserService(db)

    def post(self):
        """
        Handles user login.
        
        This endpoint expects arguments as form data:
            * username (str, max 32 characters)
            * password (str, max 32 characters)

        Returns HTTP codes and data:
            200 return code, access_token - If user login successful
            400 return code, error msg - If password is incorrect or username, login is more than 32 characters
            404 return code, error msg - If user with provided username and password not found
        """

        args = parser.parse_args(req=request)

        username, password = args["username"], args["password"]

        # Validation
        if len(username) > 32 or len(password) > 32:
            return {"msg": "Username or password too long (max 32 characters)"}, 400

        user = self.user_service.get_user_by_username(username)
        
        if user is None:
            return {"msg": "User does not exist"}, 404
        
        if not user.check_password(password):
            return {"msg": "Wrong password"}, 400
        
        token = create_access_token(identity=user)

        response = jsonify({"access_token": token})
        set_access_cookies(response, token)

        return response


class Logout(Resource):
    """
    Logout Resource
    
    Provides an endpoint for user logout.

    Methods:
        `post(self)`
            Handles POST requests for user logout.
    """

    user_service = UserService(db)

    def post(self):
        """Handles user logout by clearing JWT cookies."""

        response = jsonify({"msg": "ok"})
        unset_jwt_cookies(response)

        return response
