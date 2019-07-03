"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
from ai_acc_quality.result import Error, Result
from locust import Locust, HttpLocust, TaskSet, task

import os
import json

os.environ["EVENTHUB_NAMESPACE"] = "myns"
os.environ["EVENTHUB_NAME"] = "myeh"
os.environ["EVENTHUB_KEY"] = "mykey"
from simulator import DeviceSimulator
from unittest.mock import Mock

class TestSimulator(object):
    """
    Test Suite against Results and Errors Objects
    """

    def test_simulator(self):
        """
        Tests to ensure the assembly object can be converted to json properly
        """
        h = Mock(HttpLocust)
        t = Mock(TaskSet)
        w = DeviceSimulator(t)
        w.sendData()
        posts = w.client.post.call_args_list
        assert len(posts) == 1
        post = posts[0]
        assert post[0][0] == "/myeh/messages?timeout=60&api-version=2014-01"
        payload = json.loads(post[1]["data"])
        assert "serial_number" in payload
        assert len(payload["telemetry"]) == 1
