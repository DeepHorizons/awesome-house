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
import forms.event_forms

logger = logging.getLogger(__name__)


@app.route('/events', methods=['GET', 'POST'])
def events():
    newEventForm = forms.event_forms.NewEventForm()
    if flask.request.method == 'POST':
        if newEventForm.validate_on_submit():
            name = newEventForm.name.data
            date = newEventForm.date.data
            description = newEventForm.description.data
            logger.debug('Adding event, name {}; date {}; description {}'.format(name, date, description))
            event = models.Event(name=name,
                                 date_time=date,
                                 description=description)
            event.save()
            flask.flash('Successfully added event', 'success')
    events = models.Event.select().order_by(models.Event.date_time.asc()).where(models.Event.date_time >= datetime.datetime.combine(datetime.date.today(), datetime.time()))
    todos = models.Todo.select()
    events_with_todos = peewee.prefetch(events, todos)
    return flask.render_template('events.html', title='Events', events=events_with_todos, event_form=newEventForm)


@app.route('/events/by-id/<int:event_id>', methods=['GET', 'POST'])
def event_by_id(event_id):
    try:
        event = models.Event.get(models.Event.id == event_id)
    except peewee.DoesNotExist:
        return flask.render_template('event/event-by-id.html', error='Event id {} does not exit'.format(event_id))
    return flask.render_template('event/event-by-id.html', event=event)


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
