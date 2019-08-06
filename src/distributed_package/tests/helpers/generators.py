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

def generate_widget() -> Widget:
    w = Widget()
    w.serial_number = "devserial1"
    w.factory_id = "kitty hawk"
    w.line_id = "1"
    w.telemetry = generate_telemetry_list(10)
    w.classification = generate_classification()
    return w
