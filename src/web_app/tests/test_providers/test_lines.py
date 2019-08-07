# -*- coding: utf-8 -*-
"""
@Author: David Crook
@Author-Email: DaCrook@Microsoft.com
"""
import webapp.providers.lines as lines
from webapp.providers.connections import get_db_cxn

class TestLinesProvider(object):
    """
    Test Suite against widgets provider
    """

    def test_get_lines_overview(self):
        """
        Test to ensure we can get a widget
        """
        cnxn = get_db_cxn()
        overview = lines.get_line_overviews(cnxn, "kitty hawk")
        assert(type(overview) is dict)
    