"""
login module
"""

# Project imports
import flask
import logging
import flask_login
import peewee

# Local imports
from __init__ import app
import models
import forms.login_forms
import misc.login_functions as login_functions

logger = logging.getLogger(__name__)


@app.route('/login/check', methods=['POST'])
def login_check():
    flask_error_message = "Username or password incorrect"

    form = forms.login_forms.LoginForm(prefix='login_')
    if form.validate_on_submit():
        login_name = form.login_name.data
        user = login_functions.User.get(login_name)
        if user:
            if user.is_authorized:
                password = login_functions.get_password_hash(form.password.data, user.salt)
                if password == user.password:
                    flask_login.login_user(user)
                    logger.debug('User {}; Successfully logged in '.format(login_name))
                    flask.flash('Successfully logged in', category='success')
                else:
                    flask.flash(flask_error_message, category='danger')
            else:
                logger.warning('User {} attempted to login without being authorized'.format(login_name))
                flask.flash('Your account has not yet been authorized. Please bug someone about it.')
        else:
            logger.warning('User does not exist: {}'.format(login_name))
            flask.flash(flask_error_message, category='danger')
    else:
        logger.warning('Form is not valid: {}'.format(form.login_name.data))
        flask.flash(flask_error_message, category='danger')

    return flask.redirect(flask.url_for('index'))


@app.route('/logout')
def logout():
    if flask_login.current_user.is_authenticated:
        logger.debug('user {} Logging out'.format(flask_login.current_user.login_name))
        flask_login.logout_user()
        flask.flash('Successfully logged out', category='success')
    return flask.redirect(flask.url_for('index'))


@app.route('/login/settings', methods=['GET', 'POST'])
@flask_login.login_required
def login_settings():
    form = forms.login_forms.SettingsForm()
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            phone_number = form.phone_number.data
            phone_number = login_functions.format_phone_number(phone_number or '')
            email_me = form.email_me.data

            logger.debug('Updating user settings: Login name: {} |Name: {} |email: {} |Phone: {} |email me?: {}'.format(flask_login.current_user.login_name, name, email, phone_number, email_me))

            user = models.User.get(models.User.login_name == flask_login.current_user.login_name)
            user.name = name
            user.email = email
            user.phone_number = login_functions.format_phone_number(phone_number)
            user.email_me = email_me
            user.save()

            flask.flash('Settings changed successfully', 'success')
            return flask.redirect('/login/settings')
        else:
            # Form not valid
            logger.warning('User {} invalid form data'.format(flask_login.current_user.login_name))
            flask.flash('Invalid data submitted', category='danger')
    elif flask.request.method == 'GET':
        form.name.data = flask_login.current_user.name
        form.email.data = flask_login.current_user.email
        form.phone_number.data = flask_login.current_user.phone_number
        form.email_me.data = flask_login.current_user.email_me

    flask.flash('Phone number currently does nothing')  # TODO fix this
    return flask.render_template('settings.html', form=form)


@app.route('/login/register', methods=['GET', 'POST'])
def login_register():
    if not flask_login.current_user.is_authenticated:
        form = forms.login_forms.RegisterForm()
        if flask.request.method == 'POST':
            if form.validate_on_submit():
                login_name = form.login_name.data
                password = form.password.data
                name = form.name.data
                email = form.email.data
                phone_number = form.phone_number.data
                email_me = form.email_me.data

                logger.debug('Registering new user: Login name: {} |Password: {}|Name: {} |email: {} |Phone: {} |email me?: {}'.format(login_name, password, name, email, phone_number, email_me))  # TODO records password in log, remove this

                # Password
                password, salt = login_functions.gen_password(password)
                logger.debug('pass hash is {}'.format(password))

                try:
                    models.User(name=name,
                                login_name=login_name,
                                salt=salt,
                                password=password,
                                email_me=email_me,
                                email=email).save()
                except peewee.IntegrityError as e:
                    logger.debug(e)
                    problem_field = str(e)[str(e).find('.')+1:]

                    if problem_field in form.__dict__:
                        logger.warning('Problem was {}'.format(problem_field))
                        getattr(form, problem_field).errors.append('This entry already exists, please choose a new one')
                    else:
                        raise e
                else:
                    flask.flash('Successfully made account', category='success')
                    return flask.redirect(flask.url_for('index'))
        elif flask.request.method == 'GET':
            flask.flash('Phone number currently does nothing')  # TODO fix this
        return flask.render_template('register.html', form=form)
    else:  # The user is authenticated
        return flask.redirect(flask.url_for('index'))


@app.route('/login/admin', methods=['GET', 'POST'])
@flask_login.login_required
def login_admin():
    if flask_login.current_user.is_admin:
        if flask.request.method == 'POST':
            form = forms.login_forms.UserForm()
            if form.validate_on_submit():
                # Authorization
                # Get all form data about authorization
                authorized_list = [i for i in flask.request.form if 'authorized' in i]
                authorized_list_ids = []  # temp list for the id's in the list
                for i in authorized_list:
                    user_id = i[:i.find('_')]
                    authorized_list_ids.append(user_id)

                # Update Authorized list
                models.User.update(authorized=True).where(models.User.id.in_(authorized_list_ids)).execute()
                models.User.update(authorized=False).where(models.User.id.not_in(authorized_list_ids) &
                                                           (models.User.admin == False)).execute()

                logger.debug('User {} updated the authorized list;\n{} authorized'.format(flask_login.current_user.login_name,
                                                                                     authorized_list_ids))
                flask.flash('Users statuses changed', category='success')
            else:
                logger.warning('User {}; Error on Admin form;\n {}'.format(flask_login.current_user.login_name, form.errors))
            flask.redirect(login_admin)

        # On other requests
        users = models.User.select().order_by(models.User.authorized).dicts()
        users_forms = [forms.login_forms.UserForm()]
        for user in users:
            tmpForm = forms.login_forms.UserForm(None, prefix=str(user['id'])+'_')  # Adds <id>_ to all data for later retrieval
            for field in tmpForm:
                field.data = user.get(field.name[field.name.find('_')+1:])  # Get properties off of the user
            users_forms.append(tmpForm)

        return flask.render_template('admin.html', forms=users_forms)

    else:  # The user is not an admin
        return flask.redirect(flask.url_for('index'))
