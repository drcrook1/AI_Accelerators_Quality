"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from flask import Blueprint, render_template
from webapp.providers.connections import get_db_cxn
import webapp.providers.factories as f_provider
import json

factories = Blueprint("factories", __name__)

@factories.route("/api/v1/factories/overview", methods=["GET"])
def overview():
    f_ids = ["kitty hawk", "nags head"]
    cnxn = get_db_cxn()
    return f_provider.get_all_overviews(cnxn, f_ids)

@factories.route("/api/v1/factories/lines/overview", methods=["GET"])
def lines_overview():
    raise NotImplementedError()
