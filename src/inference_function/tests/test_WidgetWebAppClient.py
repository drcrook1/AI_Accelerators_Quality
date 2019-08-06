"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
import json
import os
import random
from datetime import datetime
from unittest.mock import Mock, patch

import requests
from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

from ProcessTelemetry.WidgetWebAppClient import WidgetWebAppClient


class TestWidgetWebAppClient(object):
    """
    Test Suite against event WidgetWebAppClient
    """

    @patch.object(requests, 'post')
    def test_post(self, mockPost):

        input_widget = generate_widget()
        c = WidgetWebAppClient(requests, "http://example.com")

        c.post(input_widget)

        mockPost.assert_called_once_with(
            "http://example.com/api/v1/live/badwidget",
            data=Matcher(checkPost),
            headers={'Content-type': 'application/json'},
            )

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
    w.classification = generate_classification()
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
    classification.classified_time = datetime.utcnow()
    classification.mean = 1.0
    classification.std = 2.0
    classification.std_dist = 1.0
    classification.threshold = 0.5
    return classification


class Matcher:
    def __init__(self, matcher):
        self.matcher = matcher
    def __eq__(self, arg):
        return self.matcher(arg)
