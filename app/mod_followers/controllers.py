# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort, jsonify
from datetime import datetime
# Get InstaLoader instance
from instaloader import instaloader, BadCredentialsException, InvalidArgumentException, TwoFactorAuthRequiredException, \
    ProfileNotExistsException
# Import the database object from the main app module
from app import db, login_required

# Import module forms
from app.mod_followers.forms import SearchFollowersForm

# Import module models (i.e. User)
from app.mod_followers.models import Follower, Batch

L = instaloader.Instaloader()

# Define the blueprint: 'followers', set its url prefix: app.url/followers
mod_followers = Blueprint('followers', __name__, url_prefix='/followers')

def fetchFollowers( username, password, searchedUser):

    L.login(username, password)  # (login)

    batch = Batch( user = searchedUser ,created_at = datetime.utcnow())
    db.session.add(batch)
    db.session.commit()

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, searchedUser) 
    for follower in profile.get_followers():
        followerObject = Follower(userid = follower.userid,
            username = follower.username,
            full_name = follower.full_name,
            follower_for = searchedUser,
            batch_id = batch.id 
        )
        db.session.add(followerObject)

    db.session.commit()
    return batch.id

@mod_followers.route('/', methods = [ 'POST' ])
@login_required
def followers():
    """Route for starting fetching followers from instagram"""
    form = SearchFollowersForm()
    if form.validate_on_submit():
        try:
            batch_id = fetchFollowers(form.loginName.data, form.password.data, form.searchUser.data)
            message = {
                'message': 'Followers Fetched Successfuly',
                'batch_id' : batch_id
            }
            resp = jsonify(message)
            resp.status_code = 200
            return resp
        except BadCredentialsException:
            message = {
                'message': 'Bad login',
                'code': 'BadLogin'
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        except InvalidArgumentException:
            message = {
                'message': 'User doesn\'t exist',
                'code': 'BadUser'
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        except TwoFactorAuthRequiredException:
            message = {
                'message': 'This account is protected by two factor authentication',
                'code': 'TwoFactorAuth'
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp
        except ProfileNotExistsException:
            message = {
                'message': 'The Searched user doesn\'t exist',
                'code': 'SearchedNotExist'
            }
            resp = jsonify(message)
            resp.status_code = 400
            return resp         
    else:
        message = {
            'message': 'There are some validation errors',
            'errors' : form.errors
        }
        resp = jsonify(message)
        resp.status_code = 400
        return resp       
@mod_followers.route('/batches/<batch_id>', methods = [ 'GET' ])
@login_required
def batches(batch_id = 0):
    """Route for getting the followers for a batch"""
    followers = Follower.query.filter_by(batch_id = batch_id ).all()
    data = {
        'followers' : [z.to_json() for z in followers]
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp

@mod_followers.route('/batches/', methods = [ 'GET' ])
@login_required
def all_batches(batch_id = 0):
    """Route for getting all batches"""
    batches = Batch.query.order_by(Batch.id.desc()).all()
    data = {
        'batches' :  [z.to_json() for z in batches]
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp