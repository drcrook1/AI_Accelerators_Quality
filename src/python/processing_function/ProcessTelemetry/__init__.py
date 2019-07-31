import logging

import azure.functions as func
import random
from datetime import datetime

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

def main(event: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                 event.get_body().decode('utf-8'))

    w = Widget.from_json(event.get_body().decode('utf-8'))

    classification = Widget_Classification()
    classification.classified_time = datetime.utcnow()
    classification.mean = random.randrange(0.0, 100.0)
    classification.std = random.randrange(0.0, 2.0)
    classification.std_dist = random.randrange(0.0, 3.0)
    classification.threshold = random.randrange(0.0, 100.0)
    w.classification = classification

    result = w.to_json()
    return result
