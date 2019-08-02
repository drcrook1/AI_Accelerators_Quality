import logging

import azure.functions as func
import random
from datetime import datetime

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

def main(event: func.EventHubEvent):

    w = Widget.from_json(event.get_body().decode('utf-8'))

    c = Widget_Classification()
    c.classified_time = datetime.utcnow()
    c.mean = random.randrange(1, 100)
    c.std = random.randrange(1, 2)
    c.std_dist = random.randrange(1, 3)
    c.threshold = random.randrange(1, 100)
    w.classification = c

    result = w.to_json()

    logging.info('Python EventHub trigger processed an event: %s', result)

    return result
