import flask_wtf
import wtforms


def phone_number_validator(form, field):
    # TODO allow different types of phone numbers
    allowable_lengths = [10, 11]

    # Sanitization
    if any(x in field.data for x in ('-', ' ')):
        if '-' in field.data:
            data = ''.join(field.data.split('-'))
        else:
            data = ''.join(field.data.split())
    else:
        data = field.data

    # Length
    if not len(data) in allowable_lengths:
        raise wtforms.ValidationError('Incorrect length of phone number')
    return


class SettingsForm(flask_wtf.Form):
    name = wtforms.StringField(None, [wtforms.validators.Length(max=32), wtforms.validators.DataRequired()],
                               description='The name you prefer to go by')
    email = wtforms.StringField(None, [wtforms.validators.Length(max=64),
                                          wtforms.validators.Email(), wtforms.validators.DataRequired()],
                                description='This is the email you will receive notifications to')
    phone_number = wtforms.StringField(None, [wtforms.validators.Optional(), phone_number_validator],
                                       description='This is the phone number you will receive reminders to',)
    email_me = wtforms.BooleanField(None, description='Do you want to receive emails?')


class LoginForm(flask_wtf.Form):
    login_name = wtforms.StringField(None, [wtforms.validators.Length(max=64), wtforms.validators.DataRequired()],
                                     description='Your login name')
    password = wtforms.PasswordField(None, [wtforms.validators.Length(max=64), wtforms.validators.DataRequired()],
                                     description='Your password')


class RegisterForm(LoginForm, SettingsForm):
    pass


class UserForm(flask_wtf.Form):
    """ Used for the admin page
    """
    name = wtforms.StringField(description='The name you prefer to go by')
    admin = wtforms.BooleanField(description='Is the user an admin?')
    authorized = wtforms.BooleanField(description='Is the user authorized?')
