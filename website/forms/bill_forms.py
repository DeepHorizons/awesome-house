import flask_wtf
import wtforms


class PaymentForm(flask_wtf.Form):
    token = wtforms.StringField(description="Your venmo userID or leave blank to signify paying cash")
