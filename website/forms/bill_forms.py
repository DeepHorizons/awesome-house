import flask_wtf
import wtforms


class PaymentForm(flask_wtf.Form):
    token = wtforms.StringField(description="Your venmo userID or leave blank to signify paying cash")


class BillForm(flask_wtf.Form):
    due = wtforms.DateField(None, [wtforms.validators.DataRequired()], format='%Y-%m-%d',
                            description='The date the bill is due')
    name = wtforms.StringField(None, [wtforms.validators.DataRequired()])
    amount = wtforms.FloatField(None, [wtforms.validators.DataRequired(), wtforms.validators.NumberRange(0, 5000)])
    description = wtforms.StringField(None, [wtforms.validators.Length(max=4096), wtforms.validators.Optional()],
                                      description='A description of the bill', widget=wtforms.widgets.TextArea())
