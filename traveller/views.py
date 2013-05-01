from flask import g, Blueprint, render_template, request
from google.appengine.api import users


views = Blueprint("views", __name__)


@views.before_request
def get_user():
    g.user = users.get_current_user()


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
