"""
Index for the website
"""

# Project imports
import flask
import logging
import datetime
import flask_login

# Local imports
from __init__ import app
import models
from models import Todo, Event
import forms.login_forms
import forms.event_forms

logger = logging.getLogger(__name__)


@app.route('/')
def index():
    tasks = Todo.select().where((Todo.event == None) &
                                (Todo.deleted == False) &
                                (
                                    (Todo.done == False) |
                                    (Todo.date_done > (datetime.date.today() - datetime.timedelta(days=7))))
                                )
    nearing_events = Event.select().order_by(Event.date_time.asc()).\
        where((Event.deleted == False) &
              (Event.date_time.between(
                  datetime.datetime.combine(datetime.date.today(), datetime.time()),
                  datetime.datetime.today() + datetime.timedelta(31))
              )
              )
    new_todo_form = forms.event_forms.NewTodoForm(formdata=None)
    return flask.render_template('index.html', title='Home', todos=tasks, events=nearing_events, todo_form=new_todo_form)


@app.before_request
def before_request():
    flask.g.db = models.db
    if not flask_login.current_user.is_authenticated:
        flask.g.login_form = forms.login_forms.LoginForm(prefix='login_')
    models.before_request_handler(flask.g.db)
    return


@app.teardown_request
def teardown_request(exception):
    db = getattr(flask.g, 'db', None)
    if db is not None:
        models.after_request_handler(db)
    return
