import logging

import azure.functions as func
import random
from datetime import datetime, timezone
import pypyodbc
import os
from ProcessTelemetry.WidgetSqlDAO import WidgetSqlDAO
from ProcessTelemetry.WidgetTableDAO import WidgetTableDAO
import uuid
import requests

from azure.storage import CloudStorageAccount
from azure.storage.table import TableService, Entity

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification


def connectODBC():
    return pypyodbc.connect(os.environ['SqlDatabaseConnectionString'])

def connectTable():
    return TableService(connection_string=os.environ['TableStorageConnectionString'])

def webServerEndpoint():
    return os.environ['SignalIOServerHttpEndpoint']

def main(event: func.EventHubEvent):

    w = Widget.from_json(event.get_body().decode('utf-8'))

    w.classification = classify_widget(w)

    (result, good) = w.classification.is_good()
    assert result.success
    rowId = uuid.uuid4().hex

    if not good:
        sqlDao = WidgetSqlDAO(connectODBC)
        sqlDao.persistWidget(w, rowId)
        sqlDao.disconnect()

    # Create a sample entity to insert into the table
    tableDao = WidgetTableDAO(connectTable(), "Predictions")
    tableDao.persistWidget(w, rowId)

    result = w.to_json()

    # Warning: has side-effect to clear telemetry list, ust be last action in function
    w.telemetry.clear()

    endpoint = "goodwidget" if good else "badwidget"
    headers = {'Content-type': 'application/json'}
    endpoint_url = "{}/api/v1/live/{}".format(webServerEndpoint(), endpoint)
    try:
        r:requests.Response = requests.post(endpoint_url, data=w.to_json(), headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.exception(e)


    logging.info('Python EventHub trigger processed an event: %s', result)

    return result

def classify_widget(w:Widget):
    c = Widget_Classification()
    c.classified_time = datetime.utcnow()
    c.mean = random.randrange(1, 100)
    c.std = random.randrange(1, 2)
    c.std_dist = random.randrange(1, 3)
    c.threshold = random.randrange(1, 100)
    return c