import logging

import azure.functions as func
from .run import run
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def main(event: func.EventHubEvent):
    event_json = event.get_body().decode('utf-8')
    run(event_json)
