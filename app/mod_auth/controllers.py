# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

# Import password / encryption helper tools
from werkzeug.security  import check_password_hash, generate_password_hash
from flask_security import login_required

# Import the database object from the main app module
from app import db, SQLAlchemyUserDatastore, Security, app

# Import module forms
from app.mod_auth.forms import CustomLoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User, Role

import flask_login

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=CustomLoginForm)

@mod_auth.route('/user', methods = [ 'GET' ])
@login_required
def get_user_info():
    """get user infos"""
    user = flask_login.current_user
    user_data = {
        'roles': [role.name for role in user.roles]
    }
    resp = jsonify(user_data)
    resp.status_code = 200
    return resp

# Seeds the database
@app.before_first_request
def seed():
    exists = db.session.query(db.exists().where(User.username == 'admin')).scalar()
    if not exists:
        user_datastore.create_role(name='admin')
        user_datastore.create_role(name='superadmin')
        user_datastore.create_user(username='admin', password='QamPam$^m^', roles=['admin'])
        user_datastore.create_user(username='superadmin', password='QamPam$^m^', roles=['superadmin','admin'])
        db.session.commit()