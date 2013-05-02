from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from google.appengine.api import users

from traveller import models, forms


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

    journey_query = models.Journey.all()
    journey_query.ancestor(g.user)
    # TODO: pagination
    journeys = journey_query.run(limit=10)

    return render_template(
        "home.html",
        journeys=journeys,
    )


@views.route("/journey/new", methods=["GET", "POST"])
def new_journey():
    form = forms.JourneyForm(request.form)
    if request.method == "POST" and form.validate():
        journey = models.Journey(
            parent=g.user,
            title=form.title.data,
        )
        journey.put()
        return redirect(url_for(".journey", id=journey.key().id()))
    return render_template("journey_new.html", form=form)


@views.route("/journey/<int:id>")
def journey(id):
    journey = models.Journey.get_by_id(id, parent=g.user)
    return render_template("journey.html", journey=journey)


@views.route("/preferences", methods=["GET", "POST"])
def preferences():
    form = forms.PreferencesForm(request.form, nickname=g.user.nickname)
    if request.method == "POST" and form.validate():
        if g.user.nickname != form.nickname.data:
            g.user.nickname = form.nickname.data
            g.user.put()
        flash("preferences saved")
        return redirect(url_for(".preferences"))
    return render_template("preferences.html", form=form)
