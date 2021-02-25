# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo, InputRequired

from flask_security.forms import LoginForm

class CustomLoginForm(LoginForm):
    email = StringField('Username', [InputRequired()])
    def validate(self):
        # Put code here if you want to do stuff before login attempt
        response = super(CustomLoginForm, self).validate()

        # Put code here if you want to do stuff after login attempt
        return response