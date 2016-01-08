import flask
import logging
import flask_login
from functools import wraps
import requests

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


def charge_venmo(access_token, charged_user_id, note, amount, audience='friends'):
    url = 'https://api.venmo.com/v1/payments'
    payload = {'access_token': access_token,
               'user_id': charged_user_id,
               'note': note,
               'amount': amount,
               'audience': audience}

    response = requests.post(url, payload)
    return response.json()


def venmo_get_payment_info(access_token, payment_id):
    url = 'https://api.venmo.com/v1/payments/{}?access_token={}'.format(payment_id, access_token)
    response = requests.get(url)
    return response.json()
