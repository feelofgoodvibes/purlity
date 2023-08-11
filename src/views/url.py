from src.service.url import URLService
from flask import render_template, abort, redirect
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

def view_short_url(short_url: str):
    try:
        url = url_service.get_url(short_url)
    except ValueError:
        abort(404)

    return render_template("url.html", url=url)