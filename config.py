# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 4

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "hVeOzxiyWpNkYTa0jCRVD7K57LDMTxrA"

# Secret key for signing cookies
SECRET_KEY = "NS1pv2W7AaPVR3X5hGuxUyLdZ7vVJdK6"

SECURITY_PASSWORD_SALT = "7MfQ8NdpZ1lr8bt4ODAsNrkdiacibBO2"

WTF_CSRF_CHECK_DEFAULT = False
WTF_CSRF_ENABLED = False
SECURITY_USER_IDENTITY_ATTRIBUTES = "username"
