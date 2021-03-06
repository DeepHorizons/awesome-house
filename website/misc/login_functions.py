import flask
import logging
import flask_login
import peewee
import flask_login
from functools import wraps
import bcrypt

from __init__ import app
import models

logger = logging.getLogger(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    """ This is the user class that is used for Flask-Login
    It should have all the properties of the User class in
    models.py
    """
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
            self.phone_number = user.phone_number
            self.table_id = user.id
        return

    @classmethod
    def get(cls, login_name):
        try:
            return cls(login_name)
        except LookupError:
            return None


# Add the is_ property for all the permission types
def gen_func(permission):
    """Generate a function that is used to check for that specific permission"""
    def func(self):
        try:
            models.Permission.select().join(models.PermissionType).switch(models.Permission).join(models.User).where(
                    (models.Permission.permission == permission) & (models.User.login_name == self.login_name)
            ).get()
        except peewee.DoesNotExist:
            return False
        else:
            return True
    return func
try:
    for p_type in models.PERMISSION_TYPE:
        prop_func = property(gen_func(models.PERMISSION_TYPE[p_type]))
        setattr(User, 'is_' + p_type, prop_func)
except:
    pass


@login_manager.user_loader
def load_user(login_name):
    return User.get(login_name)


def get_password_hash(password, hashed):
    """Generate the password hash given the plaintext of the password and a salt
    The salt can be a bcrypt pasword hash"""
    return bcrypt.hashpw(password.encode(), hashed.encode()).decode()


def gen_password(password):
    """Generate a password hash given the plaintext of the password"""
    return get_password_hash(password, bcrypt.gensalt(12).decode())


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not flask_login.current_user.is_authenticated:
            return app.login_manager.unauthorized()
        elif not flask_login.current_user.is_admin:  # TODO somehow use the flask_login.login_required function
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def format_phone_number(phone_number):
    """
    Takes in a phone number and formats it with hyphens
    Can accept 10 or 11 digit numbers
    TODO make the formatter accept different types of numbers

    :param phone_number: string of a US phone number
    :return: a string of a properly formated number
    """
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace(' ', '')
    if len(phone_number) == 10:
        return '-'.join((phone_number[:3], phone_number[3:6], phone_number[6:]))
    elif len(phone_number) == 11:
        return '-'.join((phone_number[0], phone_number[1:4], phone_number[4:7], phone_number[7:]))
    else:
        return phone_number
