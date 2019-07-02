"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Result, Error
from ai_acc_quality.data_models.base_model import Base_Model
from ai_acc_quality.data_models.telemetry import Telemetry
from typing import List, Tuple, Dict
import json
from datetime import datetime

class Widget_Classification(Base_Model):
    """
    class which defined the characteristics of a widget classification
    """
    std_dist : float = None
    std : float = None
    mean : float = None
    threshold : float = None
    classified_time : datetime = None

    def is_good(self) -> Tuple[Result, bool]:
        """
        Returns True for good and False for bad
        """
        good = True
        if(self.std_dist > self.threshold):
            good = False
        return Result(True), good

    def to_dict(self) -> Tuple[Result, Dict]:
        d = {}
        d["std_dist"] = self.std_dist
        d["std"] = self.std
        d["mean"] = self.mean
        d["threshold"] = self.threshold
        return Result(True), d

    def to_json(self) -> Tuple[Result, str]:
        _, d = self.to_dict()
        s = json.dumps(d)
        return Result(True), s        

class Widget(Base_Model):
    """
    Class defining the widget being manufactured
    """
    serial_number : str = None
    telemetry : List[Telemetry] = None
    classification : Widget_Classification = None

    def to_dict(self) -> Tuple[Result, Dict]:
        d = {}
        d["serial_number"] = self.serial_number
        telies = self.telemetry
        if(telies is not None):
            d["telemetry"] = [tel.to_dict()[1] for tel in telies]
        else:
            d["telemetry"] = None
        if(self.classification is not None):
            _, d["classification"] = self.classification.to_dict()
        else:
            d["classification"] = None
        return Result(True), d

    def to_json(self) -> Tuple[Result, str]:
        _, d = self.to_dict()
        s = json.dumps(d)
        return Result(True), s
