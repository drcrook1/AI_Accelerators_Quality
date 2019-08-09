"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Error, Result
from ai_acc_quality.data_models.widget import Widget
from helpers.generators import generate_widget
import json
import ast

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
        w2 = Widget.from_json(s)
        assert(w.serial_number == w2.serial_number)
        w2_json = w2.to_json()
        assert(type(w2_json) is str)
        json_obj_version = json.loads(w2_json)
        assert(type(json_obj_version["classification"]["is_good"]) is bool)

    def test_widget_no_classification(self):
        """
        Tests to ensure the assembly object can be converted to json properly
        """
        w = generate_widget()
        w.classification = None
        s = w.to_json()
        assert(type(s) is str)
        w2 = Widget.from_json(s)
        assert(w.serial_number == w2.serial_number)
        w2_json = w2.to_json()
        assert(type(w2_json) is  str)
        assert w2.line_id == "1"
    
    def test_many_widgets_to_json(self):
        widgets = [generate_widget().to_json() for i in range(0,10)]
        js = json.dumps(widgets)
        assert(type(js) is str)

    def test_with_nones(self):
        w = generate_widget()
        w.telemetry = None
        w.classification = None
        s = w.to_json()
        assert(type(s) is str)
