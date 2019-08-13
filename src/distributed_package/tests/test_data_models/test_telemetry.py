"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Error, Result
from ai_acc_quality.data_models.widget import Widget
from helpers.generators import generate_widget
from ai_acc_quality.data_models.telemetry import Telemetry
import json
from datetime import datetime


class TestTelemetry(object):
    """
    Test Suite against Telemetry
    """

    def test_telemetry(self):
        """
        Tests to ensure the telemetry object can be composed properly
        """
        tel = {}
        tel["voltage"] = 23.0
        tel["amperage"] = 23.0
        tel["ambient_temp"] = 34.2
        tel["ambient_humidity"] = 34.2
        tel["flux_capacitance"] = 1.0
        tel["time_stamp"] = str(datetime.utcnow())
        tel_obj = Telemetry.from_dict(tel)
        assert(tel_obj.voltage == 23.0)