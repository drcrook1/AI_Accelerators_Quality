"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from flask import Blueprint, render_template
from webapp.providers.connections import get_db_cxn
import json

factories = Blueprint("factories", __name__)

@factories.route("/api/v1/factories/count", methods=["GET"])
def count():
    raise NotImplementedError()

@factories.route("/api/v1/factories/overview", methods=["GET"])
def overview():
    raise NotImplementedError()

@factories.route("/api/v1/factories/lines/overview", methods=["GET"])
def lines_overview():
    raise NotImplementedError()
