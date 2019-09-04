"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
import os
from ai_acc_quality.ml.widget_classifier import WidgetClassifier
from ai_acc_quality.data_models.widget import Widget
from ai_acc_quality.connectors.storage import get_db_cxn, get_tbl_cnxn
import requests
import logging

def webServerEndpoint():
    return os.environ['SignalIOServerHttpEndpoint']

def post_bad_widget_to_web(widget : Widget):
    url = os.environ['SignalIOServerHttpEndpoint']
    widget.telemetry = None
    w_json = widget.to_json()
    requests.post(url, json=w_json)
    logging.info("#### --- PROCESSED ANOMALY WIDGET --- ####")
    return True

def run(event_json):
    logging.info("received message")
    widget = Widget.widget_from_json(event_json)
    classifier = WidgetClassifier()
    classifier.load_model()
    widget.classification = classifier.predict(widget)
    widget.classification.std_dist = 99.0
    try:
        if(widget.classification.is_good is False):
            post_bad_widget_to_web(widget)
        widget.persist_sql(get_db_cxn())
        widget.persist_table(get_tbl_cnxn())
        logging.info("completed widget: {}".format(widget.serial_number))
    except Exception as e:
        logging.error(str(e))
