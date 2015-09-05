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
        task_id = int(flask.request.form['id'])
        status = True if flask.request.form['status'] == 'true' else False
    except KeyError:
        logger.debug('Key error: {0}'.format(flask.request.form))
        return flask.jsonify()

    logger.debug('Updating ID {0} to status {1}'.format(task_id, status))
    date_done = None
    if status is True:
        date_done = datetime.date.today()
    models.Todo.update(done=status, date_done=date_done).where(models.Todo.id == task_id).execute()

    return flask.jsonify(date_done=date_done)
