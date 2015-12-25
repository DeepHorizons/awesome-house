"""
Index for the website
"""

# Project imports
import flask
import logging
import flask_login

# Local imports
from __init__ import app
import models
import forms.bill_forms
import misc.bill_functions as bill_functions
import misc.common as common

logger = logging.getLogger(__name__)


@app.route('/bills')
@bill_functions.bills_required
def bills():
    return flask.render_template('/bills/bills.html', title='Bills')


@app.route('/bills/settings', methods=['GET', 'POST'])
@bill_functions.bills_required
def bill_payment_settings():
    # Determining if user has already submitted a form
    payment_entry = list(models.PaymentMethod.select(models.PaymentMethod, models.User).join(models.User).where(models.User.login_name == flask_login.current_user.login_name))
    payment_form = forms.bill_forms.PaymentForm() if payment_entry else None

    if flask.request.method == 'POST':
        method = flask.request.form.get('_method', '').upper()
        if method == 'PUT':
            models.PaymentMethod.get_or_create(user=flask_login.current_user.table_id)
            _next = flask.request.form['next']
            if _next:
                return common.redirect_back('/bills/settings')
        else:
            # TODO find a way to handle multiple paymentMethods
            payment_entry[0].token = payment_form.token.data
            payment_entry[0].save()
        _next = flask.request.form['next']
        if _next:
            return common.redirect_back('/bills/settings')
    else:
        if payment_form:
            payment_form.token.data = payment_entry[0].token
    return flask.render_template('/bills/settings.html', payment_entry=payment_entry, payment_form=payment_form)
