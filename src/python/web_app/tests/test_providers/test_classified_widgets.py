# -*- coding: utf-8 -*-
"""
@Author: David Crook
@Author-Email: DaCrook@Microsoft.com
"""

from helpers import data_helpers
from webapp.providers.classified_widget import get_widget

class TestClassifiedWidgetsProvider(object):
    """
    Test Suite against widgets provider
    """

    def test_get_widget(self):
        """
        Test to ensure we can get a widget
        """
        cursor = data_helpers.get_db_cxn()
        widget = get_widget(cursor, serial_number="w1")
        f_id = widget.factory_id
        assert(f_id == "kitty hawk")
        is_good = widget.is_good
        assert(is_good is True)
