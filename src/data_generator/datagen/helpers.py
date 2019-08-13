#!/bin/env python
"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
from azure.eventhub import EventHubClient, EventData, Sender
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from ai_acc_quality.data_models.telemetry import Telemetry
import random
from typing import List
from datetime import datetime
import time
import os

def generate_telemetry() -> Telemetry:
    t = Telemetry()
    t.ambient_humidity = random.randrange(0.0, 100.0)
    t.ambient_temp = random.randrange(0.0, 120.0)
    t.amperage = random.random()
    t.voltage = random.random()
    t.flux_capacitance = random.random()
    t.time_stamp = datetime.utcnow()
    return t

def generate_telemetry_list(quantity : int) -> List[Telemetry]:
    return [generate_telemetry() for i in range(0, quantity)]

def generate_classification() -> Widget_Classification:
    classification = Widget_Classification()
    classification.classified_time = datetime.utcnow()
    classification.mean = 1.0
    classification.std = 2.0
    classification.std_dist = 1.0
    classification.threshold = 0.5
    return classification

def generate_widget(is_anomaly=False) -> Widget:
    w = Widget()
    w.serial_number = "devserial1"
    w.factory_id = "kitty hawk"
    w.line_id = "1"
    w.telemetry = generate_telemetry_list(10)
    w.classification = generate_classification()
    return w

def get_event_hub():
    conn_str = os.environ["EVENT_HUB_CONN_STRING"]
    hub_path = os.environ["EVENT_HUB_PATH"]
    client = EventHubClient.from_connection_string(conn_str, hub_path)
    sender = client.add_sender(partition="0")
    return client, sender

def push_to_event_hub(sender : Sender, widgets : List[Widget], sleep=0):
    for widget in widgets:
        sender.send(EventData(widget.to_json()))
        time.sleep(sleep)
    return True

