# -*- coding: utf-8 -*-
"""
@Author: David Crook
@Author-Email: DaCrook@Microsoft.com
"""
import datagen.helpers as helpers

class TestHelpers(object):
    """
    Test Suite against widgets provider
    """

    def test_push_msg(self):
        """
        Test to ensure we can get a widget
        """
        hub, sender = helpers.get_event_hub()
        hub.run()
        widgets = []
        widgets.append(helpers.generate_widget(is_anomaly=True))
        for i in range(0,10):
            widgets.append(helpers.generate_widget())
        res = helpers.push_to_event_hub(sender, widgets)
        assert(res is True)
    
    