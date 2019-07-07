"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
import datetime
import json

import azure.functions as func

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget
from ai_acc_quality.result import Error, Result

from . import main


class TestFunction(object):
    """
    Test Suite against Inference Function
    """

    def test_function(self):
        """
        Tests to ensure the function generates an event containing
        the enriched input event
        """

        deviceIndex = 152
        deviceId = 'contoso://device-id-{0}'.format(deviceIndex)

        t = Telemetry()
        t.voltage = 10
        t.time_stamp = datetime.datetime.utcnow()

        w = Widget()
        w.serial_number = deviceId
        w.telemetry = [t]
        (result, w_json) = w.to_json()
        assert result.success

        event = func.EventHubEvent(body=w_json.encode('utf-8'), partition_key=deviceId)
        out = main(event)

        o = Widget.from_dict(json.loads(out))
        assert o.serial_number == deviceId
