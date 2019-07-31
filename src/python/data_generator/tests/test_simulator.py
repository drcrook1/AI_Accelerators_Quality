"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
import json
import os
from unittest.mock import Mock

from locust import TaskSet

#Settings for DeviceSimulator class
os.environ["EVENTHUB_NAMESPACE"] = "myns"
os.environ["EVENTHUB_NAME"] = "myeh"
os.environ["EVENTHUB_KEY"] = "mykey"

import locustfile
from locustfile import DeviceSimulator


class TestSimulator(object):
    """
    Test Suite against event Data Generator
    """

    def test_simulator(self):
        """
        Tests to ensure the generator posts events to event hub
        """

        mockParent = Mock(TaskSet)
        simulator = DeviceSimulator(mockParent)
        simulator.sendData()
        posts = simulator.client.post.call_args_list
        assert len(posts) == 1
        post = posts[0]
        assert post[0][0] == "/myeh/messages?timeout=60&api-version=2014-01"
        payload = json.loads(post[1]["data"])
        assert "serial_number" in payload
        assert len(payload["telemetry"]) == 1
