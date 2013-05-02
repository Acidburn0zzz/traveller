from flask import g
from flask.ext import wtf
from wtforms import TextField, validators, ValidationError

from traveller.models import Traveller



class PreferencesForm(wtf.Form):
    nickname = TextField('Nickname', [validators.Required(),
                                      validators.Length(min=3, max=50)])

    def validate_nickname(form, field):
        if field.data == g.user.nickname:
            return

        q = Traveller.all(keys_only=True)
        q.filter("nickname =", field.data)
        if q.count(limit=1) != 0:
            raise ValidationError("that nickname is already taken")


class JourneyForm(wtf.Form):
    title = TextField('Name', [validators.Required(),
                               validators.Length(min=3, max=50)])
