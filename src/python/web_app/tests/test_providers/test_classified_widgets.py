# -*- coding: utf-8 -*-
"""
@Author: David Crook
@Author-Email: DaCrook@Microsoft.com
"""
from webapp.providers.classified_widget import get_widget, get_bad_widgets
from webapp.providers.connections import get_db_cxn

class TestClassifiedWidgetsProvider(object):
    """
    Test Suite against widgets provider
    """

    def test_get_widget(self):
        """
        Test to ensure we can get a widget
        """
        cnxn = get_db_cxn()
        widget = get_widget(cnxn, serial_number="w1")
        f_id = widget.factory_id
        assert(f_id == "kitty hawk")
        is_good = widget.classification.is_good
        assert(is_good is True)

    def test_get_bad_widgets(self):
        """
        Test to ensure we can get bad widgets
        """
        cnxn = get_db_cxn()
        bad_widgets = get_bad_widgets(cnxn)
        assert(len(bad_widgets) > 1)

    def test_get_bad_widgets_to_json(self):
        """
        Ensures returns proper json string
        """
        cnxn = get_db_cxn()
        bad_widgets = get_bad_widgets(cnxn, to_json=True)
        assert(type(bad_widgets) is str)