"""
Index for the website
"""

# Project imports
import flask
import logging
import datetime

logger = logging.getLogger(__name__)

# Local imports
from __init__ import app
import models


@app.route('/')
def index():
    tasks = models.Todo.select().where((models.Todo.event == None) & ((models.Todo.done == False) |
                                        (models.Todo.date_done > (datetime.date.today() - datetime.timedelta(days=7)))))
    nearing_events = models.Event.select().order_by(models.Event.date.asc()).where(models.Event.date.between(datetime.date.today(),
                                                datetime.date.today() + datetime.timedelta(7)))
    return flask.render_template('index.html', title='Home', todos=tasks, events=nearing_events)


@app.before_request
def before_request():
    flask.g.db = models.db
    models.before_request_handler(flask.g.db)
    return


@app.teardown_request
def teardown_request(exception):
    db = getattr(flask.g, 'db', None)
    if db is not None:
        models.after_request_handler(db)
    return
