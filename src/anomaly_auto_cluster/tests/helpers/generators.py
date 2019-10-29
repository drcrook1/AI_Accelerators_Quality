"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Result, Error
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from ai_acc_quality.data_models.telemetry import Telemetry
import random
from datetime import datetime
from typing import List
from uuid import uuid4
import uuid

def generate_telemetry(is_anomaly=False) -> Telemetry:
    t = Telemetry()
    t.ambient_humidity = random.randrange(0.0, 100.0)
    t.ambient_temp = random.randrange(0.0, 100.0)
    t.amperage = random.randrange(0.0, 100.0)
    if(is_anomaly):
        t.voltage = random.randrange(0.0, 50.0)
        t.flux_capacitance = random.randrange(0.0, 50.0)
    else:
        t.voltage = random.randrange(65.0, 100.0)
        t.flux_capacitance = random.randrange(65.0, 100.0)
    t.time_stamp = datetime.utcnow()
    return t

def generate_telemetry_list(quantity : int, is_anomaly=False) -> List[Telemetry]:
    return [generate_telemetry(is_anomaly=is_anomaly) for i in range(0, quantity)]

def generate_classification() -> Widget_Classification:
    classification = Widget_Classification()
    classification.classified_time = datetime.utcnow()
    classification.mean = 1.0
    classification.std = 2.0
    classification.std_dist = 1.0
    classification.threshold = 0.5
    classification.is_good = True
    return classification

def generate_widget(is_anomaly=False) -> Widget:
    w = Widget()
    w.serial_number = str(uuid.uuid4())
    factories = ["kitty hawk", "nags head", "seattle", "miami"]
    w.factory_id = random.choice(factories)
    line_ids = ["1", "2", "3"]
    w.line_id = random.choice(line_ids)
    w.telemetry = generate_telemetry_list(10, is_anomaly=is_anomaly)
    w.classification = generate_classification()
    return w
