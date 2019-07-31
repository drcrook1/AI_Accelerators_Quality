"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Error, Result
from ai_acc_quality.data_models.widget import Widget
from helpers.generators import generate_widget
import json

class TestWidgets(object):
    """
    Test Suite against Results and Errors Objects
    """

    def test_widget(self):
        """
        Tests to ensure the assembly object can be converted to json properly
        """
        w = generate_widget()
        s = w.to_json()
        assert(type(s) is str)
    
    def test_many_widgets_to_json(self):
        widgets = [generate_widget().to_json() for i in range(0,10)]
        js = json.dumps(widgets)
        assert(type(js) is str)
