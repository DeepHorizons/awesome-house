"""
Index for the website
"""

# Project imports
import flask
import logging
import flask_login
import peewee

# Local imports
from __init__ import app
import models
import forms.bill_forms
import misc.bill_functions as bill_functions
import misc.common as common

logger = logging.getLogger(__name__)


@app.route('/bills', methods=['GET', 'POST'])
@bill_functions.bills_required
def bills():
    new_bill_form = forms.bill_forms.BillForm()
    if flask.request.method == 'POST':
        if new_bill_form.validate_on_submit():
            try:
                new_bill = models.Bill(due=new_bill_form.due.data,
                                       name=new_bill_form.name.data,
                                       amount=new_bill_form.amount.data,
                                       maintainer=flask_login.current_user.table_id,
                                       description=new_bill_form.description.data,
                                       private=new_bill_form.private.data)
                new_bill.save()
            except Exception as e:
                flask.flash('Problem submitting bill', 'danger')
                logger.critical('Cannot save bill form: {}'.format(e))
                return flask.redirect(flask.url_for('bills'))
            else:
                flask.flash('Successfully added bill', 'success')

            list_of_charges = [(int(charge[charge.index('_') + 1:]), float(flask.request.form[charge])) for charge in flask.request.form if charge.startswith('user_')]
            list_of_charges = [(x, y if y >= 0 else 0) for x, y in list_of_charges]  # make sure value amounts are 0 or more
            for user_id, amount in list_of_charges:
                payment_method = models.PaymentMethod.get(models.PaymentMethod.user == user_id)
                charge = models.Charges(
                    bill=new_bill,
                    payment_method=payment_method,
                    amount=amount,
                )
                charge.save()
                # TODO charge online

            return flask.redirect(flask.url_for('bills'))
        # TODO There may need to be a redirect here

    # TODO Improve all of this
    payment_methods = list(models.PaymentMethod.select(models.PaymentMethod, models.User).join(models.User).join(models.Permission).where(models.Permission.permission == models.PERMISSION_TYPE['bills']))  # TODO figure out how to handle multiple payment methods
    outstanding_user_charges = models.Charges.select(models.Charges, models.PaymentMethod, models.Bill).join(models.PaymentMethod).switch(models.Charges).join(models.Bill).where((models.PaymentMethod.user == flask_login.current_user.table_id) & (models.Charges.paid == False)).execute()
    outstanding_charges = models.Charges.select().where(models.Charges.paid == False).execute()
    outstanding_bills_ids = [charge.bill.id for charge in outstanding_charges]
    outstanding_bills = models.Bill.select().where(models.Bill.id.in_(outstanding_bills_ids) & (models.Bill.private == False)).order_by(+models.Bill.due).execute()

    return flask.render_template('/bills/bills.html', title='Bills', new_bill_form=new_bill_form, payment_methods=payment_methods, user_charges=outstanding_user_charges, outstanding_bills=outstanding_bills)


@app.route('/bills/by-id/<int:bill_id>')
@bill_functions.bills_required
def bills_by_id(bill_id):
    try:
        bill = models.Bill.get(models.Bill.id == bill_id)
    except peewee.DoesNotExist:
        logger.warning('User {}; Attempted access to bill ID {} that does not exist'.format(flask_login.current_user.login_name, bill_id))
        return flask.render_template('bills/bills-by-id.html', error='Bill id {} does not exit'.format(bill_id))
    return flask.render_template('bills/bills-by-id.html', bill=bill)


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


@app.route('/charge/by-id/<int:charge_id>')
@bill_functions.bills_required
def charge_by_id(charge_id):
    try:
        charge = models.Charges.get(models.Charges.id == charge_id)
        error=None
    except peewee.DoesNotExist:
        logger.warning('User {}; Attempted access to charge ID {} that does not exist'.format(flask_login.current_user.login_name, charge_id))
        error = 'Bill id {} does not exit'.format(charge_id)
    return flask.render_template('bills/charge-by-id.html', charge=charge, error=error)
