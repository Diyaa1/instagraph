# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort, jsonify

from datetime import datetime

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db, SQLAlchemyUserDatastore, Security, app, login_required

# Import module forms
from app.mod_followers.forms import SearchFollowersForm

# Import module models (i.e. User)
from app.mod_followers.models import Follower, Batch

# Define the blueprint: 'followers', set its url prefix: app.url/followers
mod_followers = Blueprint('followers', __name__, url_prefix='/followers')


def fetchFollowers():

    batch = Batch( created_at = datetime.utcnow())
    db.session.add(batch)
    db.session.commit()

    user_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    full_name = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]

    profile_pic_url = 'https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg'
    follower_for = 'Diyaa'

    for i in range(len(user_names)):
        follower = Follower( username = user_names[i], full_name = full_name[i], profile_pic_url = profile_pic_url, follower_for = follower_for, batch_id = batch.id )
        db.session.add(follower)
        
    db.session.commit()
    return batch.id

@mod_followers.route('/', methods = [ 'POST' ])
@login_required
def followers():
    form = SearchFollowersForm()
    if form.validate_on_submit():
        batch_id = fetchFollowers()
        message = {
            'message': 'Followers Fetched Successfuly',
            'batch_id' : batch_id
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
        
@mod_followers.route('/batches/<batch_id>', methods = [ 'GET' ])
@login_required
def batches(batch_id = 0):
    followers = Follower.query.filter_by(batch_id = batch_id ).all()
    data = {
        'followers' : [z.to_json() for z in followers]

    }
    print(followers)
    resp = jsonify(data)
    resp.status_code = 200
    return resp
