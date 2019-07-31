"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from flask import Blueprint, render_template
from webapp.providers.classified_widget import get_bad_widgets, get_widget
from webapp.providers.connections import get_db_cxn
import json

widgets = Blueprint("widgets", __name__)

@widgets.route("/badwidgets")
def badwidgets():
    cnxn = get_db_cxn()
    badwidgets = get_bad_widgets(cnxn, to_json=True)
    return badwidgets