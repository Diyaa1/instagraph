# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort, jsonify

# Import password / encryption helper tools
from werkzeug.security  import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db, SQLAlchemyUserDatastore, Security, app, login_required

# Import module forms
from app.mod_followers.forms import SearchFollowersForm

# Import module models (i.e. User)
from app.mod_followers.models import Follower

# Define the blueprint: 'followers', set its url prefix: app.url/followers
mod_followers = Blueprint('followers', __name__, url_prefix='/followers')

@mod_followers.route('/', methods = [ 'POST' ])
@login_required
def followers():
    form = SearchFollowersForm()
    if form.validate_on_submit():
        "Start Routine Here"
        message = {
            'message': 'Followers Fetched Successfuly',
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    else:
        message = {
            'message': 'There are some validation errors',
            'errors' : form.errors
        }
        resp = jsonify(message)
        resp.status_code = 400
        return resp
        
