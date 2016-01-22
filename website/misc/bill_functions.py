import flask
import logging
import flask_login
from functools import wraps
import requests

from __init__ import app

logger = logging.getLogger(__name__)

VENMO_URL = 'https://api.venmo.com/v1'
if app.config.get('TESTING', None):
    VENMO_URL = 'https://sandbox-api.venmo.com/v1'


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
    url = VENMO_URL + '/payments'
    payload = {'access_token': access_token,
               'user_id': charged_user_id,
               'note': note,
               'amount': -(float(amount)),
               'audience': audience}

    response = requests.post(url, payload).json()
    return look_for_error(response)


def venmo_get_payment_info(access_token, payment_id):
    url = VENMO_URL + '/payments/{}?access_token={}'.format(payment_id, access_token)
    response = requests.get(url).json()
    return look_for_error(response)


def look_for_error(response):
    if 'error' in response:
        logger.critical('Venmo access error code {}: {}'.format(response['error']['code'], response['error']['message']))
        raise LookupError('Improper access to venmo')
    return response


def update_charge_status(charge):
    token = charge.payment_method.token if charge.payment_method.token else charge.bill.maintainer.payment_methods[0].token
    response_json = venmo_get_payment_info(token, charge.online_charge_id)

    if response_json['data']['status'] == 'settled':
        charge.paid = True
        charge.save()
    return
