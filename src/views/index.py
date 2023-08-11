from flask_jwt_extended import get_current_user, jwt_required
from flask import render_template
from src.service.url import URLService
from src.schemas.url import URLFilters
from src.database import db


@jwt_required(optional=True)
def index():
    user = get_current_user()
    urls = None

    if user is not None:
        url_service = URLService(db)
        urls = url_service.get_all_urls(URLFilters(user=user.id))

    return render_template("index.html", user=user, urls=urls)
