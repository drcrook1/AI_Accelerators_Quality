"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from flask import Blueprint, render_template
import json

security = Blueprint("security", __name__)

@security.route("/test")
def test():
    result = {"something" : "some thing"}
    return json.dumps(result)