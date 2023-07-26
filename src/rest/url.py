from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from src.database import db
from src.service.url import URLService
from src.schemas import url as url_schemas


class URL(Resource):
    url_service = URLService(db)

    @jwt_required(optional=True)
    def get(self, short_url: str):
        current_user = get_current_user()

        try:
            url = self.url_service.get_url(short_url)
        except ValueError as e:
            return {"error": str(e)}
        
        if current_user is None:
            return jsonify(url_schemas.URL.from_orm(url).dict())
        else:
            return jsonify(url_schemas.URLAuthenticated.from_orm(url).dict())


