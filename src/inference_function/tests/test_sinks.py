# -*- coding: utf-8 -*-
"""
@Author: David Crook
@Author-Email: DaCrook@Microsoft.com
"""
from ProcessTelemetry.run import post_bad_widget_to_web
from helpers.generators import generate_widget

class TestLinesProvider(object):
    """
    Test Suite against function sinks
    """

    def test_web_sink(self):
        """
        Test to ensure we can get a widget
        """
        widget = generate_widget()
        post_bad_widget_to_web(widget)
        assert(True)
    

    