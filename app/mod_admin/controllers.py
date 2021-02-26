# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort, jsonify

from datetime import datetime

import os

# Import the database object from the main app module
from app import db, celery, app, login_required
from flask_security import roles_required

from app.mod_admin.models import Setting
from app.mod_auth.models import User
from app.mod_auth.controllers import user_datastore

from app.mod_admin.forms import SaveSettings, SaveHiddenSettings
from sqlalchemy.exc import IntegrityError


# Define the blueprint: 'admin', set its url prefix: app.url/admin
mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/settings', methods = [ 'POST' ])
@login_required
@roles_required('superadmin')
def save_settings():
    """save settings"""
    form = SaveSettings()
    if form.validate_on_submit():
        login_name = form.loginName.data
        password = form.password.data

        login_name_setting = Setting.query.get("USER")
        login_name_setting.value = login_name

        login_password_setting = Setting.query.get("PASSWORD")
        login_password_setting.value = password

        db.session.commit()
        try:
            os.remove("bsession")
        except OSError:
            pass
        #Save Here
        resp = jsonify({
            'msg': 'Saved'
        })
        resp.status_code = 200
        return resp       
    resp = jsonify({
        'msg': 'There are some validation errors'
    })
    resp.status_code = 400
    return resp   

@mod_admin.route('/settings', methods = [ 'GET' ])
@login_required
@roles_required('superadmin')
def get_settings():
    """returns all settings"""
    settings = Setting.query.all()
    settings_dic = [z.to_json() for z in settings]
    keys =  [ k['key'] for k in settings_dic ]
    values =  [ v['value'] for v in settings_dic ]
    resp = jsonify(dict(zip(keys, values)))
    resp.status_code = 200
    return resp


@mod_admin.route('/hsettings', methods = [ 'POST' ])
@login_required
@roles_required('superadmin')
def save_hidden_settings():
    """save settings"""
    form = SaveHiddenSettings()
    if form.validate_on_submit():
        is_fixed = form.isFixed.data
        fixed_name = form.fixedWinner.data

        login_name_setting = Setting.query.get("FIXED")
        login_name_setting.value = "1" if is_fixed else "0" 

        login_password_setting = Setting.query.get("FIXEDUSER")
        login_password_setting.value = fixed_name

        db.session.commit()

        #Save Here
        resp = jsonify({
            'msg': 'Saved'
        })
        resp.status_code = 200
        return resp       
    resp = jsonify({
        'msg': 'There are some validation errors'
    })
    resp.status_code = 400
    return resp   

@mod_admin.route('/hsettings', methods = [ 'GET' ])
@login_required
@roles_required('superadmin')
def get_hidden_settings():
    """returns all settings"""
    settings = Setting.query.all()
    settings_dic = [z.to_json() for z in settings]
    keys =  [ k['key'] for k in settings_dic ]
    values =  [ v['value'] for v in settings_dic ]
    resp = jsonify(dict(zip(keys, values)))
    resp.status_code = 200
    return resp

# Create a default user on app start if user doesn't exist
@app.before_first_request
def create_settings():
    defualt_user_name = db.session.query(db.exists().where(Setting.key == 'USER')).scalar()
    if not defualt_user_name:
        setting = Setting( key = "USER" ,value = "default")
        db.session.add(setting)
        db.session.commit()

    defualt_user_password = db.session.query(db.exists().where(Setting.key == 'PASSWORD')).scalar()
    if not defualt_user_password:
        setting = Setting( key = "PASSWORD" ,value = "default")
        db.session.add(setting)
        db.session.commit()

    defualt_fixed_user = db.session.query(db.exists().where(Setting.key == 'FIXEDUSER')).scalar()
    if not defualt_fixed_user:
        setting = Setting( key = "FIXEDUSER" ,value = "default")
        db.session.add(setting)
        db.session.commit()
    
    defualt_is_fixed = db.session.query(db.exists().where(Setting.key == 'FIXED')).scalar()
    if not defualt_is_fixed:
        setting = Setting( key = "FIXED" ,value = "0")
        db.session.add(setting)
        db.session.commit()
@mod_admin.route('/users', methods = [ 'GET' ])
@login_required
@roles_required('superadmin')
def get_users():
    """returns all users"""
    users = User.query.join(User.roles)
    users_list = [z.to_json() for z in users]
    resp = jsonify(users_list)
    resp.status_code = 200
    return resp
@mod_admin.route('/users/<user_id>', methods = [ 'DELETE' ])
@login_required
@roles_required('superadmin')
def delete_user(user_id):
    """Deletes a user by id"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    resp = jsonify([])
    resp.status_code = 200
    return resp
@mod_admin.route('/users/<user_id>', methods = [ 'GET' ])
@login_required
@roles_required('superadmin')
def get_user(user_id):
    """Gets a user by id"""
    user = User.query.filter(User.id == user_id).first()
    resp = jsonify(user.to_json())
    resp.status_code = 200
    return resp
@mod_admin.route('/users/<user_id>', methods = [ 'post' ])
@login_required
@roles_required('superadmin')
def update_user(user_id):
    """update a user by id"""
    data = request.json
    username = data["username"]
    password = data["password"]
    user = User.query.filter(User.id == user_id).first()
    if username:
        user.username = username
    if password:
        user.password = password
    try:
        db.session.commit()
        resp = jsonify([])
        resp.status_code = 200
        return resp
    except IntegrityError:
        db.session.rollback()
        resp = jsonify({
            'errorMsg' : "User name is already used."
        })
        resp.status_code = 400
        return resp
@mod_admin.route('/users', methods = [ 'post' ])
@login_required
@roles_required('superadmin')
def create_user():
    """creates a new user"""
    data = request.json
    username = data["username"]
    password = data["password"]
    user_datastore.create_user(username=username, password=password, roles=['admin'])
    try:
        db.session.commit()
        resp = jsonify([])
        resp.status_code = 200
        return resp
    except IntegrityError:
        db.session.rollback()
        resp = jsonify({
            'errorMsg' : "User name is already used."
        })
        resp.status_code = 400
        return resp