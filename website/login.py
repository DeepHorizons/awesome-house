"""
login module
"""

# Project imports
import flask
import logging
import flask.ext.login
import peewee
import hashlib

logger = logging.getLogger(__name__)

# Local imports
from __init__ import app
import models

login_manager = flask.ext.login.LoginManager()
login_manager.init_app(app)


class User(flask.ext.login.UserMixin):
    def __init__(self, login_name):
        try:
            user = models.User.get(models.User.login_name == login_name)
        except peewee.DoesNotExist:
            logger.warning("User with login_name '{0}' not found".format(login_name))
            raise LookupError('User not found')
        else:
            self.id = login_name
            self.name = user.name
            self.login_name = user.login_name
            self.email_me = user.email_me
            self.email = user.email
            self.password = user.password
            self.salt = user.salt
            self.phone_number = user.phone_number
        return

    @classmethod
    def get(cls, login_name):
        try:
            return cls(login_name)
        except LookupError:
            return None


@login_manager.user_loader
def load_user(login_name):
    return User.get(login_name)

# TODO make this the registration page
@app.route('/login')
def login():
    return '''
        <form action="/login/check" method="post">
            <p>Username: <input name="username" type="text"></p>
            <p>Password: <input name="password" type="password"></p>
            <input type="submit">
        </form>
    '''


@app.route('/login/check', methods=['POST'])
def login_check():
    flask_error_message = "Username or password incorrect"

    user = User.get(flask.request.form['username'])
    if user:
        password = flask.request.form['password']
        password = hashlib.sha256(password.encode() + user.salt.encode()).hexdigest()
        if password == user.password:
            flask.ext.login.login_user(user)
            flask.flash('Successfully logged in', category='success')
        else:
            flask.flash(flask_error_message, category='warning')
    else:
        flask.flash(flask_error_message, category='warning')
    return flask.redirect(flask.url_for('index'))


@app.route('/logout')
def logout():
    if flask.ext.login.current_user.is_authenticated:
        flask.ext.login.logout_user()
        flask.flash('Successfully logged out', category='success')
    return flask.redirect(flask.url_for('index'))


@app.route('/login/settings', methods=['GET', 'POST'])
def login_settings():
    if flask.ext.login.current_user.is_authenticated:
        print(flask.request.method)
        if flask.request.method == 'POST':
            print(flask.request.form)
            name = flask.request.form['name']
            email = flask.request.form['email']
            phone_number = flask.request.form['phone_number']
            email_me = 'email_me' in flask.request.form
            print('Name: {} email: {} Phone: {} email me?: {}'.format(name, email, phone_number, email_me))
            flask.flash('Settings changed successfully', 'success')
            return flask.redirect('/login/settings')
        flask.flash('Phone number currently does nothing')  # TODO fix this
        return flask.render_template('settings.html')
    return flask.redirect(flask.url_for('index'))
