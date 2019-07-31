"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from flask import Flask

def create_app():
    app = Flask(__name__)

    from webapp.apis.views import views
    app.register_blueprint(views)

    from webapp.apis.security import security
    app.register_blueprint(security)

    from webapp.apis.widgets import widgets
    app.register_blueprint(widgets)

    return app
