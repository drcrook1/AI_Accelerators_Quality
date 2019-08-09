import logging

import azure.functions as func
import random
from datetime import datetime, timezone
import pyodbc
import os
from .WidgetSqlDAO import WidgetSqlDAO
from .WidgetTableDAO import WidgetTableDAO
from .WidgetWebAppClient import WidgetWebAppClient
from .MLModelStorageDAO import MLModelStorageDAO
import uuid
import requests

from azure.storage import CloudStorageAccount
from azure.storage.table import TableService
from azure.storage.blob import BlockBlobService

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification


def connectODBC():
    return pyodbc.connect(os.environ['SqlDatabaseConnectionString'])

def connectTable():
    return TableService(connection_string=os.environ['TableStorageConnectionString'])

def webServerEndpoint():
    return os.environ['SignalIOServerHttpEndpoint']

def requestsObj():
    return requests

def connectModel() -> MLModelStorageDAO:
    blobService = BlockBlobService(connection_string=os.environ['ModelsStorageConnectionString'])
    return MLModelStorageDAO(blobService, "models")

def main(event: func.EventHubEvent):

    w = Widget.from_json(event.get_body().decode('utf-8'))

    w.classification = connectModel().classify_widget(w)

    (result, good) = w.classification.is_good()
    assert result.success
    rowId = uuid.uuid4().hex

    webapp_client = WidgetWebAppClient(requestsObj(), webServerEndpoint())
    webapp_client.post(w)

    sqlDao = WidgetSqlDAO(connectODBC)
    sqlDao.persistWidget(w, rowId)
    sqlDao.disconnect()

    # Create a sample entity to insert into the table
    tableDao = WidgetTableDAO(connectTable(), "Predictions")
    tableDao.persistWidget(w, rowId)

    result = w.to_json()

    logging.info('Python EventHub trigger processed an event: %s', result)

    return result
