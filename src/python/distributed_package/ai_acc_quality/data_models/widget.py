"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Result, Error
from ai_acc_quality.data_models.base_model import Base_Model
from ai_acc_quality.data_models.telemetry import Telemetry
from typing import List, Tuple, Dict
from datetime import datetime
import json

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

    def from_dict(self, data):
        self.std_dist = data["std_dist"]
        self.std = data["std"]
        self.mean = data["mean"]
        self.threshold = data["threshold"]

    def to_json(self) -> str:
        """
        converts this object to a json object
        """
        _, s_dict = self.to_dict()
        return json.dumps(s_dict)

class Widget(Base_Model):
    """
    Class defining the widget being manufactured
    """
    serial_number : str = None
    factory_id : str = None
    line_id : str = None
    telemetry : List[Telemetry] = None
    classification : Widget_Classification = None

    def to_dict(self) -> Tuple[Result, Dict]:
        d = {}
        d["serial_number"] = self.serial_number
        telies = []
        for tel in self.telemetry:
            _, t_dict = tel.to_dict()
            telies.append(t_dict)
        d["telemetry"] = telies
        _, d["classification"] = self.classification.to_dict()
        return Result(True), d

    def to_json(self) -> str:
        """
        converts this object to a json object
        """
        _, s_dict = self.to_dict()
        return json.dumps(s_dict)

    @classmethod
    def from_dict(cls, data):
        w = cls()
        w.serial_number = data["serial_number"]
        w.telemetry = cls._list_from_dict(data["telemetry"], Telemetry)
        w.classification = cls._list_from_dict(data["classification"], Widget_Classification)
        return w
