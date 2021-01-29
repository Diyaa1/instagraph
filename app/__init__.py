# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from flask_wtf.csrf import CSRFProtect, generate_csrf


# Define the WSGI application object
app = Flask(__name__, static_url_path="", static_folder="static")

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_followers.controllers import mod_followers as followers_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(followers_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')
