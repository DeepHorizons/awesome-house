"""
Index for the website
"""

# Project imports
import flask
import logging
import datetime

# Local imports
from __init__ import app
import models


@app.route('/')
def index():
    tasks = models.Todo.select().where(models.Todo.event == None)  # TODO don't get done tasks if more than a week old
    nearing_events = models.Event.select().order_by(models.Event.date.asc()).where(models.Event.date.between(datetime.date.today(),
                                                datetime.date.today() + datetime.timedelta(7)))
    return flask.render_template('index.html', title='Home', tasks=tasks, events=nearing_events)


@app.route('/todo/by-id/<int:todo_id>')
def todo_by_id(todo_id):
    task = models.Todo.get(models.Todo.id == todo_id)
    return task.task

