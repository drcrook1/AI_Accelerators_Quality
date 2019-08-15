# -*- coding: utf-8 -*-
"""
@Author: David Crook
@Author-Email: DaCrook@Microsoft.com
"""
import webapp.providers.factories as factories
from webapp.providers.connections import get_db_cxn

class TestFactoriesProvider(object):
    """
    Test Suite against widgets provider
    """

    def test_anomaly_tred(self):
        """
        Test to ensure we can get a widget
        """
        cnxn = get_db_cxn()
        trend = factories.get_anomaly_trend(cnxn, "kitty hawk")
        assert(type(trend) is float)
    
    def test_factory_overview(self):
        cnxn = get_db_cxn()
        data = factories.get_factory_overview(cnxn, "kitty hawk")
        assert(type(data) is dict)

    def test_multiple_factory_overviews(self):
        cnxn = get_db_cxn()
        data = factories.get_all_overviews(cnxn)
        assert(type(data) is str)