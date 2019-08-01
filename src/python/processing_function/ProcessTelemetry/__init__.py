import logging

import azure.functions as func
import random
from datetime import datetime
import pypyodbc
import os
from ProcessTelemetry.WidgetDAO import WidgetDAO
import uuid

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

def connectODBC():
    return pypyodbc.connect(os.environ['SqlDatabaseConnectionString'])

def main(event: func.EventHubEvent):

    w = Widget.from_json(event.get_body().decode('utf-8'))

    c = Widget_Classification()
    c.classified_time = datetime.utcnow()
    c.mean = random.randrange(0.0, 100.0)
    c.std = random.randrange(0.0, 2.0)
    c.std_dist = random.randrange(0.0, 3.0)
    c.threshold = random.randrange(0.0, 100.0)
    w.classification = c

    (result, good) = c.is_good()
    assert result.success
    if not good:
        dao = WidgetDAO(connectODBC)
        dao.persistWidget(w, uuid.uuid4().hex)
        dao.disconnect()

    result = w.to_json()

    logging.info('Python EventHub trigger processed an event: %s', result)

    return result
