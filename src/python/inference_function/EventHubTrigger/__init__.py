import logging

import azure.functions as func

from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget

print("Initting")
print("Initted")
def main(event: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                 event.get_body().decode('utf-8'))
    w = Widget.from_json(event.get_body().decode('utf-8'))
    _, result = w.to_json()
    return result
