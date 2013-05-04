from flask import Blueprint, url_for, redirect
from flask.ext.oauth import OAuth
from google.appengine.api import taskqueue

from traveller import settings


latitude = Blueprint("latitude", __name__, url_prefix="/latitude")
latitude_oauth = OAuth().remote_app(
    "google",
    base_url="https://www.google.com/accounts/",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    request_token_url=None,
    request_token_params={
        "scope": "https://www.googleapis.com/auth/latitude.all.best",
        "response_type": "code",
    },
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_method="POST",
    access_token_params={
        "grant_type": "authorization_code",
    },
    consumer_key=settings.GOOGLE_CLIENT_ID,
    consumer_secret=settings.GOOGLE_CLIENT_SECRET,
)


@latitude.route("/start")
def start():
    callback=url_for('.authorized', _external=True)
    return latitude_oauth.authorize(callback=callback)


@latitude.route("/authorized")
@latitude_oauth.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    taskqueue.add(
        url=url_for(".download_data"),
        params={
            "token": access_token,
        },
    )
    return redirect(url_for('.report_progress'))


@latitude.route("/task", methods=["POST"])
def download_data():
    return "YAY"


@latitude.route("/loading")
def report_progress():
    return "things are happening!"
