import flask_wtf
import wtforms


class PaymentForm(flask_wtf.Form):
    token = wtforms.StringField()
