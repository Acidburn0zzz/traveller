from google.appengine.ext import db


class Traveller(db.Model):
    nickname = db.StringProperty(required=True)


class Journey(db.Model):
    title = db.StringProperty(required=True)
