"""
Index for the website
"""

# Project imports
import flask
import logging
import datetime
import peewee
import flask_login
from urllib.parse import urlparse, urljoin
from flask import request, url_for

# Local imports
from __init__ import app
import models
import forms.event_forms

logger = logging.getLogger(__name__)


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return flask.redirect(target)


@app.route('/events', methods=['GET', 'POST'])
@flask_login.login_required
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
@flask_login.login_required
def event_by_id(event_id):
    try:
        event = models.Event.get(models.Event.id == event_id)
    except peewee.DoesNotExist:
        return flask.render_template('event/event-by-id.html', error='Event id {} does not exit'.format(event_id))

    if flask.request.method == 'POST':
        method = flask.request.form.get('_method', '').upper()
        if method == 'PUT':
            event_form = forms.event_forms.EditEventForm()
            if event_form.validate_on_submit():
                event.name = event_form.name.data
                event.date_time = event_form.date.data
                event.description = event_form.description.data
                event.save()
                flask.flash('Event updated', 'success')
            else:
                flask.flash('Could not update event', 'danger')
        elif method == 'DELETE':
            if event.deleted:
                event.deleted = False
                message = 'Event un-deleted'
            else:
                event.deleted = True
                message = 'Event deleted'
            event.save()
            flask.flash(message, 'success')

    event_form = forms.event_forms.EditEventForm(formdata=None, name=event.name, date=event.date_time, description=event.description)
    new_todo_form = forms.event_forms.NewTodoForm(formdata=None, event=event_id)
    return flask.render_template('event/event-by-id.html', event=event, event_form=event_form, todo_form=new_todo_form)


@app.route('/todos', methods=['GET', 'POST'])
@flask_login.login_required
def todos():
    newTodoForm = forms.event_forms.NewTodoForm()
    if flask.request.method == 'POST':
        if newTodoForm.validate_on_submit():
            event = newTodoForm.event.data
            task = newTodoForm.task.data
            description = newTodoForm.description.data
            logger.debug('Adding todo, event {}; task {}; description {}'.format(event, task, description))
            todo = models.Todo(event=event,
                               task=task,
                               description=description)
            todo.save()
            flask.flash('Successfully added todo', 'success')
            next = request.form['next']
            if next:
                return redirect_back('/todos')
    all_todos = models.Todo.select()
    return flask.render_template('todo.html', title='Todo', todos=all_todos)


@app.route('/todos/by-id/<int:todo_id>', methods=['GET', 'POST'])
@flask_login.login_required
def todo_by_id(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except peewee.DoesNotExist:
        return flask.render_template('event/todo-by-id.html', error='Todo id {} does not exit'.format(todo_id))

    if flask.request.method == 'POST':
        method = flask.request.form.get('_method', '').upper()
        if method == 'PUT':
            todo_form = forms.event_forms.EditTodoForm()
            if todo_form.validate_on_submit():
                todo.task = todo_form.task.data
                todo.description = todo_form.description.data
                todo.save()
                flask.flash('Event updated', 'success')
            else:
                flask.flash('Could not update event', 'danger')
        elif method == 'DELETE':
            if todo.deleted:
                todo.deleted = False
                message = 'Event un-deleted'
            else:
                todo.deleted = True
                message = 'Event deleted'
            todo.save()
            flask.flash(message, 'success')

    edit_todo_form = forms.event_forms.EditTodoForm(task=todo.task, description=todo.description)
    return flask.render_template('event/todo-by-id.html', todo=todo, edit_todo_form=edit_todo_form)


@app.route('/todos/status', methods=['POST'])
@flask_login.login_required
def todo_status():
    """Ajax request"""
    print(flask.request.form)
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
