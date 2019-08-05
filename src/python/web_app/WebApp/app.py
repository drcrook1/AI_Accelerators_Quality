"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
from flask_socketio import SocketIO
from flask import Flask

socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    from webapp.apis.views import views
    app.register_blueprint(views)

    from webapp.apis.security import security
    app.register_blueprint(security)

    from webapp.apis.widgets import widgets
    app.register_blueprint(widgets)

    from webapp.apis.realtime import events
    app.register_blueprint(events)

    from webapp.apis.factories import factories
    app.register_blueprint(factories)

    socketio.init_app(app)

    return app
