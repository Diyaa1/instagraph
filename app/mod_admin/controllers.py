# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort, jsonify

from datetime import datetime

import os

# Import the database object from the main app module
from app import db, celery, app, login_required

from app.mod_admin.models import Setting

from app.mod_admin.forms import SaveSettings

# Define the blueprint: 'admin', set its url prefix: app.url/admin
mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

@mod_admin.route('/settings', methods = [ 'POST' ])
@login_required
def saveSettings():
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
def getSettings():
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