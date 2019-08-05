"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
from webapp.app import socketio
from flask_socketio import send, emit
from flask import Blueprint, request

events = Blueprint("events", __name__)

@socketio.on('text')
def text(message):
    print('received message: ' + str(message))

@events.route("/api/v1/live/badwidget", methods=["POST"])
def livebadwidget():
    widget_json = request.get_json()
    socketio.emit("live_badwidget", widget_json)

@events.route("/api/v1/live/goodwidget", methods=["POST"])
def livegoodwidget():
    widget_json = request.get_json()
    socketio.emit("live_goodwidget", widget_json)
