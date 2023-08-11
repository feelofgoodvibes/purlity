from src.service.url import URLService
from flask import render_template, abort, redirect, url_for
from flask_jwt_extended import jwt_required, get_current_user
from src.database import db
from src.models import Visit

url_service = URLService(db)

def goto_url(short_url: str):
    try:
        url = url_service.get_url(short_url)
    except ValueError:
        abort(404)

    url.visits.append(Visit())
    db.session.commit()

    return redirect(url.url)

@jwt_required(optional=True)
def view_short_url(short_url: str):
    if get_current_user() is None:
        return redirect(url_for("webapp.index"))

    try:
        url = url_service.get_url(short_url)
    except ValueError:
        abort(404)

    return render_template("url.html", url=url)