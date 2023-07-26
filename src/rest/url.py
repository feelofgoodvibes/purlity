from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from src.database import db
from src.service.url import URLService
from src.schemas.url import URL as URLSchema


class URL(Resource):
    url_service = URLService(db)

    @jwt_required(optional=True)
    def get(self, short_url: str):
        try:
            url = self.url_service.get_url(short_url)
            return jsonify(URLSchema.from_orm(url).dict())
        except ValueError as e:
            return {"error": str(e)}
