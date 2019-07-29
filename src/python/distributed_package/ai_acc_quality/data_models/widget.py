"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Result, Error
from ai_acc_quality.data_models.base_model import Base_Model
from ai_acc_quality.data_models.telemetry import Telemetry
from typing import List, Tuple, Dict
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
        d["telemetry"] = self._list_to_dict(self.telemetry)
        d["classification"] = self._list_to_dict(self.classification)
        return Result(True), d

    @classmethod
    def from_dict(cls, data):
        w = cls()
        w.serial_number = data["serial_number"]
        w.telemetry = cls._list_from_dict(data["telemetry"], Telemetry)
        w.classification = cls._list_from_dict(data["classification"], Widget_Classification)
        return w
