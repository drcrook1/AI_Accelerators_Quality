"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Result, Error
from ai_acc_quality.data_models.base_model import Base_Model
from ai_acc_quality.data_models.telemetry import Telemetry
from typing import List, Tuple, Dict
from datetime import datetime
import dateutil.parser as parser
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

    def is_good(self) -> bool:
        """
        Returns True for good and False for bad
        """
        good = True
        if(self.std_dist > self.threshold):
            good = False
        return good

    def to_dict(self) -> Tuple[Result, Dict]:
        d = {}
        d["std_dist"] = self.std_dist
        d["std"] = self.std
        d["mean"] = self.mean
        d["threshold"] = self.threshold
        d["classified_time"] = self.classified_time.isoformat()
        d["is_good"] = self.is_good()
        return Result(True), d

    @classmethod
    def from_dict(cls, data):
        c = cls()
        c.std_dist = data["std_dist"]
        c.std = data["std"]
        c.mean = data["mean"]
        c.threshold = data["threshold"]
        c.classified_time = parser.parse(data["classified_time"])
        return c

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
    telemetry : List[Telemetry] = []
    classification : Widget_Classification = None

    def to_dict(self) -> Tuple[Result, Dict]:
        d = {}
        d["serial_number"] = self.serial_number
        d["factory_id"] = self.factory_id
        d["line_id"] = self.line_id
        if(self.telemetry is not None):
            telies = []
            for tel in self.telemetry:
                _, t_dict = tel.to_dict()
                telies.append(t_dict)
            d["telemetry"] = telies
        if(self.classification is not None):
            _, d["classification"] = self.classification.to_dict()
        return Result(True), d

    def to_json(self) -> str:
        """
        converts this object to a json object
        """
        _, s_dict = self.to_dict()
        return json.dumps(s_dict)

    @staticmethod
    def from_dict(data):
        w = Widget()
        w.serial_number = data["serial_number"]
        w.factory_id = data["factory_id"]
        w.line_id = data["line_id"]
        w.telemetry = []
        for telemetry in data["telemetry"]:
            w.telemetry.append(Telemetry.from_dict(telemetry))
        w.classification = Widget_Classification.from_dict(data["classification"]) if "classification" in data else None
        return w

    @staticmethod
    def widget_from_json(data):
        data = json.loads(data)
        return Widget.from_dict(data)

    def persist_sql(self, cnxn):
        cursor = cnxn.cursor()
        query = """INSERT INTO [dbo].[classified_widgets](
            [serial_number], [std_dist], [std], [mean],
            [threshold], [is_good], 
            [factory_id], [line_id], [classified_time])
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (
            self.serial_number, self.classification.std_dist, self.classification.std, self.classification.mean,
            self.classification.threshold, self.classification.is_good(), 
            self.factory_id, self.line_id, self.classification.classified_time.isoformat())
        cursor.execute(query, values)
        cursor.commit()
        cursor.close()

    @staticmethod
    def generate_partition_key(factory_id, line_id):
        return factory_id + ":" + line_id

    def persist_table(self, cnxn):
        data = {
            "PartitionKey": Widget.generate_partition_key(self.factory_id, self.line_id),
            "RowKey" : self.serial_number,
            "data" : json.dumps(self.to_json())
        }
        cnxn.insert_entity("classifiedwidgets", data)

    @staticmethod
    def from_table(cnxn, factory_id, line_id, serial_number):
        entity = cnxn.get_entity("classifiedwidgets", Widget.generate_partition_key(factory_id, line_id), serial_number)
        data = json.loads(entity.data)
        widget = Widget.from_json(data)
        return widget