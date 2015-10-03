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
    name = wtforms.StringField('name', [wtforms.validators.Length(max=32), wtforms.validators.DataRequired()])
    email = wtforms.StringField('email', [wtforms.validators.Length(max=64), wtforms.validators.Email(), wtforms.validators.DataRequired()])
    phone_number = wtforms.StringField('phone number', [wtforms.validators.Optional(), phone_number_validator])
    email_me = wtforms.BooleanField()


class LoginForm(flask_wtf.Form):
    login_name = wtforms.StringField('username', [wtforms.validators.Length(max=64), wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('password', [wtforms.validators.Length(max=64), wtforms.validators.DataRequired()])


class RegisterForm(SettingsForm, LoginForm):
    pass
