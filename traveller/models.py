from google.appengine.ext import db


class Traveller(db.Model):
    nickname = db.StringProperty(required=True)
