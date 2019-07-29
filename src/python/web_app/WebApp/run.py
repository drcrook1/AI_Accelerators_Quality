"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from WebApp.app import create_app
from flask import render_template

app = create_app()

app.run(host='0.0.0.0', port=80)
