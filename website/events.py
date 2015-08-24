"""
Index for the website
"""

# Project imports
import flask
import logging

# Local imports
from __init__ import app
import models


@app.route('/events')
def events():
    return flask.render_template('events.html', title='Events')


@app.route('/todo/by-id/<int:todo_id>')
def todo_by_id(todo_id):
    task = models.Todo.get(models.Todo.id == todo_id)
    return task.task
