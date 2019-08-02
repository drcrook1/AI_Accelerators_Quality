"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
import json
import os
import ProcessTelemetry
from unittest.mock import Mock, ANY
from datetime import datetime
import pypyodbc
import azure.functions as func

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

class TestWidgetDAO(object):
    """
    Test Suite against event WidgetDAO
    """

    #from unittest.mock import patch
    #@patch('pypyodbc.Connection')
    def test_persist(self):#, mockConnection: pypyodbc.Connection):
        """
        Tests to ensure the generator posts events to event hub
        """

        input_widget = generate_widget()
        input_event = func.EventHubEvent(body=input_widget.to_json().encode())

        output_json = ProcessTelemetry.main(input_event)

        output_widget = Widget.from_json(output_json)

        assert output_widget.serial_number == input_widget.serial_number
        assert output_widget.classification.std_dist > 0

def generate_widget() -> Widget:
    w = Widget()
    w.serial_number = "devserial1"
    w.factory_id = "kitty hawk"
    w.line_id = "1"
    return w