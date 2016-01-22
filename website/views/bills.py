"""
Index for the website
"""

# Project imports
import flask
import logging
import flask_login
import peewee
import requests
import random

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
            with getattr(flask.g, 'db', models.db).atomic() as txn:
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
                    txn.rollback()
                    return flask.redirect(flask.url_for('bills'))

                list_of_charges = [(int(charge[charge.index('_') + 1:]), float(flask.request.form[charge])) for charge in flask.request.form if charge.startswith('user_')]
                list_of_charges = [(x, y if y >= 0 else 0) for x, y in list_of_charges]  # make sure value amounts are 0 or more
                maintainer_payment_method = models.PaymentMethod.get(models.PaymentMethod.user == flask_login.current_user.table_id)
                try:
                    for user_id, amount in list_of_charges:
                        # TODO handle multiple payment methods
                        payment_method = models.PaymentMethod.get(models.PaymentMethod.user == user_id)
                        charge = models.Charges(
                            bill=new_bill,
                            payment_method=payment_method,
                            amount=amount,
                        )

                        # TODO charge online
                        if payment_method.pay_online and maintainer_payment_method.pay_online and maintainer_payment_method.token:
                            response_json = bill_functions.charge_venmo(maintainer_payment_method.token, payment_method.online_user_id, new_bill.name, amount, 'private' if new_bill.private else 'friends')
                            charge.online_charge_id = response_json['data']['payment']['id']
                        charge.save()

                except Exception as e:
                    flask.flash('Problem charging users')
                    logger.critical('Cannot charge user: {}'.format(e))
                    txn.rollback()
                    return flask.redirect(flask.url_for('bills'))

            flask.flash('Successfully added bill', 'success')
            return flask.redirect(flask.url_for('bills'))
        # TODO There may need to be a redirect here

    # TODO Improve all of this
    payment_methods = list(models.PaymentMethod.select(models.PaymentMethod, models.User).join(models.User).join(models.Permission).where(models.Permission.permission == models.PERMISSION_TYPE['bills']))  # TODO figure out how to handle multiple payment methods
    outstanding_charges = models.Charges.select(models.Charges, models.PaymentMethod).join(models.PaymentMethod).where(models.Charges.paid == False).execute()

    # Get an update on all charges that were made online
    for charge in outstanding_charges:
        try:
            bill_functions.check_charge(charge)
        except LookupError:
            break

    outstanding_charges = models.Charges.select().where(models.Charges.paid == False).execute()  # Get it again if it was updated
    outstanding_user_charges = models.Charges.select(models.Charges, models.PaymentMethod, models.Bill).join(models.PaymentMethod).switch(models.Charges).join(models.Bill).where((models.PaymentMethod.user == flask_login.current_user.table_id) & (models.Charges.paid == False)).execute()
    outstanding_bills_ids = [charge.bill.id for charge in outstanding_charges]
    outstanding_bills = models.Bill.select().where(models.Bill.id.in_(outstanding_bills_ids) & (models.Bill.private == False)).order_by(+models.Bill.due).execute()

    return flask.render_template('/bills/bills.html', title='Bills', new_bill_form=new_bill_form, payment_methods=payment_methods, user_charges=outstanding_user_charges, outstanding_bills=outstanding_bills)


@app.route('/bills/by-id/<int:bill_id>')
@bill_functions.bills_required
def bills_by_id(bill_id):
    try:
        bill = models.Bill.select().join(models.Charges).switch(models.Bill).where(models.Bill.id == bill_id).get()
    except peewee.DoesNotExist:
        logger.warning('User {}; Attempted access to bill ID {} that does not exist'.format(flask_login.current_user.login_name, bill_id))
        return flask.render_template('bills/bills-by-id.html', error='Bill id {} does not exit'.format(bill_id))

    for charge in bill.charges:
        try:
            bill_functions.check_charge(charge)
        except LookupError:
            break
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
            if payment_form.pay_online.data:
                if (app.config.get('VENMO_CLIENT_ID', None) is None) or (app.config.get('VENMO_CLIENT_SECRET', None) is None):
                    flask.flash('The site is not configured to user Venmo. Contact the site administrator', 'warning')
                    logger.critical('No VENMO_CLIENT_ID or VENMO_CLIENT_SECRET set in the config')
                else:
                    state = random.randint(0, 100000)
                    payment_entry[0].token = state
                    payment_entry[0].save()
                    logger.debug('Redirecting user {} id {} to venmo to authenticate, state is {}'.format(flask_login.current_user.name, flask_login.current_user.table_id, state))
                    return flask.redirect('https://api.venmo.com/v1/oauth/authorize?client_id={}&scope={}&response_type=code&state={}'.format(app.config.get('VENMO_CLIENT_ID', None), 'make_payments%20access_profile', state))
            else:
                payment_entry[0].pay_online = payment_form.pay_online.data
                payment_entry[0].save()

        _next = flask.request.form['next']
        if _next:
            return common.redirect_back('/bills/settings')
    else:
        if payment_form:
            payment_form.pay_online.data = payment_entry[0].pay_online
    return flask.render_template('/bills/settings.html', payment_entry=payment_entry, payment_form=payment_form)


@app.route('/charge/by-id/<int:charge_id>', methods=['GET', 'POST'])
@bill_functions.bills_required
def charge_by_id(charge_id):
    try:
        charge = models.Charges.get(models.Charges.id == charge_id)
        error = None
    except peewee.DoesNotExist:
        charge = None
        logger.warning('User {}; Attempted access to charge ID {} that does not exist'.format(flask_login.current_user.login_name, charge_id))
        error = 'Bill id {} does not exit'.format(charge_id)
    else:
        if flask.request.method == 'POST':
            charge.paid = not charge.paid
            charge.save()
    return flask.render_template('bills/charge-by-id.html', charge=charge, error=error)


@app.route('/bills/venmo_redirect')
def bills_venmo_redirect():
    if 'error' in flask.request.args:
        flask.flash('The request was denied. Please retry authenticating with Venmo', 'danger')

    payment_method = models.PaymentMethod.get(models.PaymentMethod.user == flask_login.current_user.table_id)
    if (payment_method.token is None) or (flask.request.args.get('state', None) != str(payment_method.token)):
        logger.critical('CSRF Check failed in bills_venmo_redirect. Expected {} but got {}'.format(payment_method.token, flask.request.args.get('state', None)))
        flask.g.state = None
        flask.flash('Venmo CSRF Failed. Please retry', 'danger')
    else:
        user_code = flask.request.args['code']
        logger.info('User {} with id {} got the Venmo code of {}'.format(flask_login.current_user.name, flask_login.current_user.table_id, user_code))

        # Get the access token from the code
        data = {
            'client_id': app.config.get('VENMO_CLIENT_ID', None),
            'client_secret': app.config.get('VENMO_CLIENT_SECRET', None),
            'code': user_code
        }
        url = "https://api.venmo.com/v1/oauth/access_token"
        response = requests.post(url, data)
        response_dict = response.json()
        logger.info('Venmo gave the response of \n{}'.format(response_dict))

        access_token = response_dict['access_token']
        user_venmo_id = response_dict['user']['id']

        payment_method = models.PaymentMethod.get(models.PaymentMethod.user == flask_login.current_user.table_id)
        payment_method.token = access_token
        payment_method.online_user_id = user_venmo_id
        payment_method.pay_online = True
        payment_method.save()
        flask.flash('Venmo payments were successfully set up', 'success')
    return flask.redirect(flask.url_for('index'))
