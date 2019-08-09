"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
import json
import os
from ProcessTelemetry.WidgetSqlDAO import WidgetSqlDAO
from unittest.mock import Mock, ANY
from datetime import datetime
import pyodbc

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

class TestWidgetSqlDAO(object):
    """
    Test Suite against event WidgetSqlDAO
    """

    from unittest.mock import patch
    @patch('pyodbc.Connection')
    def test_persist(self, mockConnection: pyodbc.Connection):
        """
        Tests to ensure the generator posts events to event hub
        """

        dao = WidgetSqlDAO(lambda : mockConnection)
        w = generate_widget()
        dao.persistWidget(w, "myid")

        c = w.classification
        mockConnection.cursor().execute.assert_called_once_with(ANY,
            (w.serial_number, c.std_dist, c.std, c.mean,
            c.threshold, c.is_good(), "myid",
            w.factory_id, w.line_id, c.classified_time.isoformat(),))

def generate_classification() -> Widget_Classification:
    classification = Widget_Classification()
    classification.classified_time = datetime.utcnow()
    classification.mean = 1.0
    classification.std = 2.0
    classification.std_dist = 1.0
    classification.threshold = 0.5
    return classification

def generate_widget() -> Widget:
    w = Widget()
    w.serial_number = "devserial1"
    w.factory_id = "kitty hawk"
    w.line_id = "1"
    w.classification = generate_classification()
    return w