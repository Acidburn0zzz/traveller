from flask import Flask

from traveller.latitude import latitude
from traveller.views import views


app = Flask(__name__)
app.secret_key = "test"
app.register_blueprint(views)
app.register_blueprint(latitude)
app.config.from_object("traveller.settings")
