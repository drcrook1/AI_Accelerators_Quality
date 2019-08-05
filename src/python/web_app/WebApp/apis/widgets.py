"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from flask import Blueprint, render_template
from webapp.providers.classified_widget import get_bad_widgets, get_widget
from webapp.providers.connections import get_db_cxn
import json

widgets = Blueprint("widgets", __name__)

@widgets.route("/api/v1/widgets/badwidgets", methods=["GET"])
def badwidgets():
    cnxn = get_db_cxn()
    badwidgets = get_bad_widgets(cnxn, to_json=True)
    return badwidgets

@widgets.route("/api/v1/widgets/goodwidgets", methods=["GET"])
def goodwidgets():
    raise NotImplementedError()

@widgets.route("/api/v1/widgets/page/good", methods=["POST"])
def page_good():
    raise NotImplementedError()

@widgets.route("/api/v1/widgets/page/bad", methods=["POST"])
def page_bad():
    raise NotImplementedError()

@widgets.route("/api/v1/widgets/page/all", methods=["POST"])
def page_all():
    raise NotImplementedError()

@widgets.route("/api/v1/widgets/specificwidget", methods=["POST"])
def widget():
    raise NotImplementedError()

@widgets.route("/api/v1/widgets/count/total", methods=["GET"])
def count_total():
    raise NotImplementedError()

@widgets.route("/api/v1/widgets/count/bad", methods=["GET"])
def count_bad():
    raise NotImplementedError()

@widgets.route("/api/v1/widgets/count/good", methods=["GET"])
def count_good():
    raise NotImplementedError()
