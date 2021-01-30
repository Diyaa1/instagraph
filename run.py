# Run a test server.
from app import app,socketio

# app.run(host='localhost', port=8080, debug=True)
socketio.run(app, debug=True)