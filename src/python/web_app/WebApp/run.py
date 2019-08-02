"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from webapp.app import create_app
from flask import render_template
from flask_socketio import SocketIO

app = create_app()

socketio = SocketIO(app)

@socketio.on('my event')
def handle_message(message):
    print('received message: ' + str(message))

socketio.run(app, host="0.0.0.0", port=80)
#app.run(host='0.0.0.0', port=80)
