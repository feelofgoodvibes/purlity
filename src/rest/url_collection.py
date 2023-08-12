from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_current_user
from src.database import db
from src.service.url import URLService
from src.schemas import url as url_schemas


parser = reqparse.RequestParser()
parser.add_argument("url",
                    type=str,
                    help="Missing url value",
                    required=True,
                    location='form')


class URL_collection(Resource):
    """
    URL_collection Resource
    
    Provides endpoints for listing and creating URLs.

    Methods:
        get(self)
            Handles GET requests for listing URLs.
        
        post(self)
            Handles POST requests for creating a new URL.
    """

    url_service = URLService(db)

    @jwt_required()
    def get(self):
        """
        Handles listing URLs associated with the authenticated user.

        Returns:
            list: A list of URL objects in dictionary format.
        """

        current_user = get_current_user()
        filters = url_schemas.URLFilters.parse_obj(request.args)
        filters.user = current_user.id

        return jsonify([url_schemas.URLAuthenticated.from_orm(url).dict()
                for url in self.url_service.get_all_urls(filters=filters)])

    @jwt_required(optional=True)
    def post(self):
        """
        Handles the creation of a new URL.

        Returns:
            dict: A JSON response containing the newly created URL details.

        Raises:
            ValueError: If the URL creation fails.
        """

        args = parser.parse_args(req=request)

        current_user = get_current_user()
        
        try:
            created_url = self.url_service.create_url(user_id=current_user and current_user.id, url=args["url"])
        except ValueError as e:
            return {"msg": str(e)}, 400


        db.session.commit()
        return jsonify(url_schemas.URL.from_orm(created_url).dict())
