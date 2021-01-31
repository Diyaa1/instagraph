# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

from flask_security.forms import LoginForm



# Define the login form (WTForms)

# class LoginForm(Form):
#     email    = TextField('Email Address', [Email(),
#                 Required(message='Forgot your email address?')])
#     password = PasswordField('Password', [
#                 Required(message='Must provide a password. ;-)')])


class CustomLoginForm(LoginForm):
    def validate(self):
        # Put code here if you want to do stuff before login attempt
        response = super(CustomLoginForm, self).validate()

        # Put code here if you want to do stuff after login attempt
        return response