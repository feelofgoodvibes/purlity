from flask import request, abort
from flask_restful import Resource, reqparse
from src.database import db
from src.service.url import URLService
from src.schemas.url import URL as URLSchema, URLFilters

parser = reqparse.RequestParser()
parser.add_argument("url", type=str, help="Missing url value", required=True, location='form')

class URL(Resource):
    url_service = URLService(db)

    def get(self, short_url: str = None):
        if short_url:
            try:
                return URLSchema.from_orm(self.url_service.get_url(short_url)).dict()
            except ValueError as e:
                return {"error": str(e)}
        else:
            filters = URLFilters.parse_obj(request.args)
            return [URLSchema.from_orm(url).dict()
                    for url in self.url_service.get_all_urls(filters=filters)]

    def post(self, short_url: str = None):
        if short_url is not None:
            abort(405)

        args = parser.parse_args(req=request)
        created_url = self.url_service.create_url(user_id=None, url=args["url"])
        db.session.commit()
        return URLSchema.from_orm(created_url).dict()