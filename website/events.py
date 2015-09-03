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


@app.route('/events/by-id/<int:event_id>')
def event_by_id(event_id):
    event = models.Event.get(models.Event.id == event_id)
    return event.name


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if flask.request.method == 'POST':
        print('POST:', flask.request.form)
    todos = models.Todo.select()
    return flask.render_template('todo.html', title='Todo', todos=todos)


@app.route('/todo/by-id/<int:todo_id>')
def todo_by_id(todo_id):
    task = models.Todo.get(models.Todo.id == todo_id)
    return task.task


@app.route('/todo/status', methods=['POST'])
def todo_status():
    """Ajax request"""
    try:
        id = int(flask.request.form['id'])
        status = True if flask.request.form['status'] == 'true' else False
    except KeyError:
        return flask.jsonify()
    print(id, status)
    return flask.jsonify()
