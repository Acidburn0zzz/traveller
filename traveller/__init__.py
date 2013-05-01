from flask import Flask

from traveller.views import views


app = Flask(__name__)
app.register_blueprint(views)
