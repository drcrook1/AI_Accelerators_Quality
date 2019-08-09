"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
import json
import os
import random
from datetime import datetime, timezone
from unittest.mock import ANY, Mock, patch

import azure.functions as func
import pyodbc
import requests
from azure.storage.table import TableService

import ProcessTelemetry
from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from ProcessTelemetry.MLModelStorageDAO import MLModelStorageDAO


class TestProcessTelemetry(object):
    """
    Test Suite against event ProcessTelemetry
    """

    @patch('pypyodbc.Connection')
    @patch('azure.storage.table.TableService')
    def test_persist(self, mockConnection: pyodbc.Connection, mockTableService: TableService):
        """
        Tests to ensure the generator posts events to event hub
        """

        input_widget = generate_widget()
        input_event = func.EventHubEvent(body=input_widget.to_json().encode())
        mockRequests = Mock(requests)

        modelMLStorageDAO = Mock(MLModelStorageDAO)
        modelMLStorageDAO.classify_widget.return_value = generate_classification()

        ProcessTelemetry.connectODBC = lambda: mockConnection
        ProcessTelemetry.connectTable = lambda: mockTableService
        ProcessTelemetry.webServerEndpoint = lambda: "http://example.com"
        ProcessTelemetry.requestsObj = lambda: mockRequests
        ProcessTelemetry.connectModel = lambda: modelMLStorageDAO

        output_json = ProcessTelemetry.main(input_event)

        output_widget = Widget.from_json(output_json)

        assert output_widget.serial_number == input_widget.serial_number
        assert output_widget.classification.std_dist > 0
        mockRequests.post.assert_called_once_with(ANY, data=ANY, headers=ANY)


def checkPost(jsonData):
    w = Widget.from_json(jsonData)
    assert w.serial_number == "devserial1"
    assert not w.telemetry
    return True


def generate_widget() -> Widget:
    w = Widget()
    w.serial_number = "devserial1"
    w.factory_id = "kitty hawk"
    w.line_id = "1"
    w.telemetry = [generate_telemetry() for i in range(0, 202)]
    return w


def generate_telemetry() -> Telemetry:
    t = Telemetry()
    t.ambient_humidity = random.randrange(0.0, 100.0)
    t.ambient_temp = random.randrange(0.0, 120.0)
    t.amperage = random.random()
    t.voltage = random.random()
    t.flux_capacitance = random.random()
    t.time_stamp = datetime.utcnow()
    return t


def generate_classification() -> Widget_Classification:
    classification = Widget_Classification()
    classification.classified_time = datetime.fromtimestamp(
        1000000000, timezone.utc)
    classification.mean = 1.0
    classification.std = 2.0
    classification.std_dist = 1.0
    classification.threshold = 0.5
    return classification
