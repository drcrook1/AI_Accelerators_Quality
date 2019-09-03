"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Error, Result
from ai_acc_quality.data_models.widget import Widget
from helpers.generators import generate_widget
from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.ml.widget_classifier import WidgetClassifier
import json
from datetime import datetime


class TestWidgetClassifier(object):
    """
    Test Suite against the Classifier Class
    """

    def test_instantiation(self):
        """
        Tests to ensure the telemetry object can be composed properly
        """
        classifier = WidgetClassifier()
        classifier.load_model()
        assert(classifier.encoder is not None)
        assert(classifier.cluster is not None)
        assert(classifier.telemetry_keys is not None)

    def test_pre_process(self):
        classifier = WidgetClassifier()
        classifier.load_model()
        widget = generate_widget()
        processed = classifier.pre_process(widget)
        assert(processed.shape == (1,10,5))

    def test_predict(self):
        classifier = WidgetClassifier()
        classifier.load_model()
        widget = generate_widget(is_anomaly=True)
        prediction = classifier.predict(widget)
        assert(prediction.is_good is False)
        widget = generate_widget(is_anomaly=False)
        prediction = classifier.predict(widget)
        assert(prediction.is_good is True)