"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
from webapp.app import socketio
from flask_socketio import SocketIO
from flask import Blueprint

events = Blueprint("events", __name__)

@socketio.on('text')
def text(message):
    print('received message: ' + str(message))
