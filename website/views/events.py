"""
Index for the website
"""

# Project imports
import flask
import logging
import datetime
import peewee
import flask_login

# Local imports
from __init__ import app
import models

logger = logging.getLogger(__name__)


def get_count(obj):
    return obj.count()


@app.route('/events')
def events():
    events = models.Event.select()
    todos = models.Todo.select()
    events_with_todos = peewee.prefetch(events, todos)
    return flask.render_template('events.html', title='Events', events=events_with_todos, get_count=get_count)


@app.route('/events/by-id/<int:event_id>')
def event_by_id(event_id):
    event = models.Event.get(models.Event.id == event_id)
    return event.name


@app.route('/todos')
def todo():
    todos = models.Todo.select()
    return flask.render_template('todo.html', title='Todo', todos=todos)


@app.route('/todos/by-id/<int:todo_id>')
def todo_by_id(todo_id):
    task = models.Todo.get(models.Todo.id == todo_id)
    return task.task


@app.route('/todos/status', methods=['POST'])
@flask_login.login_required
def todo_status():
    """Ajax request"""
    try:
        task_id = int(flask.request.form['id'])
        status = True if flask.request.form['status'] == 'true' else False
    except KeyError:
        logger.debug('Key error: {0}'.format(flask.request.form))
        return flask.jsonify()

    logger.debug('Updating ID {0} to status {1}'.format(task_id, status))
    date_done = datetime.date.today()
    models.Todo.update(done=status, date_done=date_done if status else None).where(models.Todo.id == task_id).execute()

    return flask.jsonify(task_id=task_id, date_done=str(date_done) if status else None)
