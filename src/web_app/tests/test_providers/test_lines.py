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
        assert(len(overview) > 0)
    
    def test_get_all_line_overviews(self):
        cnxn = get_db_cxn()
        f_ids = ["kitty hawk", "nags head"]
        overviews = lines.get_all_overviews(cnxn, f_ids)
        assert(len(overviews) > 0)

    