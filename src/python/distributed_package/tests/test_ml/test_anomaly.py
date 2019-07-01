"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Error, Result
from ai_acc_quality.data_models.widget import Widget
from helpers.generators import generate_widget
from ai_acc_quality.ml.anomaly_model import Anomaly_Model

class TestAnomalyMl(object):
    """
    Test Suite against Results and Errors Objects
    """

    def test_anomaly_creation(self):
        """
        Tests to ensure the assembly object can be converted to json properly
        """
        a = Anomaly_Model("devserial1")
        assert(a is not None)
    