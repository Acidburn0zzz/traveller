from flask import g, Blueprint, render_template, request
from google.appengine.api import users

from traveller import models


views = Blueprint("views", __name__)


@views.before_request
def get_user():
    user = users.get_current_user()

    if not user:
        g.user = None
        return

    g.user = models.Traveller.get_or_insert(
        user.user_id(), nickname=user.nickname())


@views.context_processor
def inject_auth_context():
    if g.user:
        return {
            "logout_url": users.create_logout_url("/"),
        }
    else:
        return {
            "login_url": users.create_login_url(request.url),
        }


@views.route("/")
def home():
    if not g.user:
        return render_template("home_anonymous.html")
    return render_template("home.html")
