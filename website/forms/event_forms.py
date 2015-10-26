import flask_wtf
import wtforms
from wtforms.widgets import TextArea


class NewEventForm(flask_wtf.Form):
    name = wtforms.StringField(None, [wtforms.validators.Length(max=64), wtforms.validators.DataRequired()],
                               description='The name of the event')
    date = wtforms.DateTimeField(None, [wtforms.validators.DataRequired()], format='%Y-%m-%d %H:%M',
                                description='The date and time of the event')
    description = wtforms.StringField(None, [wtforms.validators.Length(max=4096), wtforms.validators.Optional()],
                                       description='A description of the event', widget=TextArea())
