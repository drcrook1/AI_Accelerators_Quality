"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
from unittest.mock import Mock, ANY
from datetime import datetime

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from ai_acc_quality.ml.score import score

class TestScoring(object):
    """
    Test Suite
    """

    def test_scoring(self):
        """
        Tests to ensure the generator posts events to event hub
        """
        w = generate_widget()
        before = datetime.utcnow()
        c = score("tests/ml/model_files/", w)
        after = datetime.utcnow()

        assert 8.55 < c.std_dist < 8.56
        assert 0.45 < c.std < 0.46
        assert 1.05 < c.mean < 1.06
        assert c.threshold == 3
        assert before < c.classified_time < after


def generate_widget() -> Widget:
    w = Widget()
    w.serial_number = "devserial1"
    w.factory_id = "kitty hawk"
    w.line_id = "1"
    w.telemetry = [generate_telemetry() for i in range(0, 2)]
    return w

def generate_telemetry() -> Telemetry:
    t = Telemetry()
    t.ambient_humidity = 1.
    t.ambient_temp = 1.
    t.amperage = 1.
    t.voltage = 1.
    t.flux_capacitance = 1.
    t.time_stamp = datetime.utcnow()
    return t
