import flask
import logging
import flask_login
from functools import wraps

from __init__ import app


def bills_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not flask_login.current_user.is_authenticated:
            return app.login_manager.unauthorized()
        elif not flask_login.current_user.is_bills:  # TODO somehow use the flask_login.login_required function
            return app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view