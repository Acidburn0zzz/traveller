from flask import Flask

from traveller.views import views


app = Flask(__name__)
app.secret_key = "test"
app.register_blueprint(views)
