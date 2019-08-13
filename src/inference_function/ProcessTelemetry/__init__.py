import logging

import azure.functions as func
from .run import run

def main(event: func.EventHubEvent):
    event_json = event.get_body().decode('utf-8')
    run(event_json)
    return True
