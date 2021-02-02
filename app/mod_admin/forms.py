# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, TextField, PasswordField, validators # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

# Define the login form (WTForms)

class SaveSettings(Form):
    loginName    = StringField(u'User Name', [validators.required(), validators.length(max=255)])
    password = StringField(u'Password', [validators.required(), validators.length(max=255)])