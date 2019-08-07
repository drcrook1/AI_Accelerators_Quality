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
        out = score("tests/ml/model_files/", w)
        std_dist : float = None
        std : float = None
        mean : float = None
        threshold : float = None
        classified_time : datetime = None

        assert out['score'] > 4.92 and out['score'] < 4.93
        assert 4.92 < out['score'] < 4.93
        assert 8.55 < out['std_dist'] < 8.56
        assert 0.45 < out['std'] < 0.46
        assert 1.05 < out['mean'] < 1.06
        assert 2.41 < out['threshold'] < 2.42


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
