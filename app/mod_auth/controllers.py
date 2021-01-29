# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security  import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db, SQLAlchemyUserDatastore, Security, app

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User, Role



# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a default user on app start if user doesn't exist
@app.before_first_request
def create_user():
    exists = db.session.query(db.exists().where(User.email == 'deaalmhamedd@gmail.com')).scalar()
    if not exists:
        user_datastore.create_user(email='deaalmhamedd@gmail.com', password='password')
        db.session.commit()



