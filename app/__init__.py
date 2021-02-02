# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from flask_wtf.csrf import CSRFProtect, generate_csrf

from celery import Celery

# Define the WSGI application object
app = Flask(__name__, static_url_path="", static_folder="static")

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='rpc',
        broker='amqp://root:246879513@localhost:5672/vhost'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_followers.controllers import mod_followers as followers_module

from app.mod_admin.controllers import mod_admin as admin_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(followers_module)
app.register_blueprint(admin_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()


# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')