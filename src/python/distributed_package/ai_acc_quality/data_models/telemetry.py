"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Result, Error
from ai_acc_quality.data_models.base_model import Base_Model
from datetime import datetime
from typing import Tuple, Dict
import json

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class Telemetry(Base_Model):
    """
    Class defining the widget being manufactured
    """
    voltage : float = None
    amperage : float = None
    ambient_temp: float = None
    ambient_humidity: float = None
    flux_capacitance : float = None
    time_stamp : datetime = None

    def to_dict(self) -> Tuple[Result, Dict]:
        d = {}
        d["voltage"] = self.voltage
        d["amperage"] = self.amperage
        d["ambient_temp"] = self.ambient_temp
        d["ambient_humidity"] = self.ambient_humidity
        d["flux_capacitance"] = self.flux_capacitance
        d["time_stamp"] = self.time_stamp.strftime(TIME_FORMAT)
        return Result(True), d

    @classmethod
    def from_dict(cls, data):
        w = cls()        
        w.voltage = data["voltage"]
        w.amperage = data["amperage"]
        w.ambient_temp = data["ambient_temp"]
        w.ambient_humidity = data["ambient_humidity"]
        w.flux_capacitance = data["flux_capacitance"]
        w.serial_number = data["serial_number"]
        w.time_stamp = datetime.strptime(data["time_stamp"], TIME_FORMAT)
        return w