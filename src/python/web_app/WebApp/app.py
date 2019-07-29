"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from flask import Flask

def create_app():
    app = Flask(__name__)

    from WebApp.apis.views import views
    app.register_blueprint(views)

    from WebApp.apis.security import security
    app.register_blueprint(security)

    return app
