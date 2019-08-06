"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from abc import ABC, abstractclassmethod
from ai_acc_quality.result import Result
from typing import Dict, Tuple
import json

class Base_Model(ABC):
    """
    Base data model all data models should inherit from
    """
    
    @abstractclassmethod
    def to_dict(self) -> Tuple[Result, Dict]:
        raise NotImplementedError()
    
    @staticmethod
    def _list_to_dict(data):
        if(data is None):
            return None
        return [datum.to_dict()[1] for datum in data]

    @staticmethod
    def _list_from_dict(data, destType):
        if(data is None):
            return None
        assert type(data) is list
        return list(map(destType.from_dict, data))

    @abstractclassmethod
    def to_json(self) -> Tuple[Result, str]:
        raise NotImplementedError()
        # result, d = self.to_dict()
        # if(result.success is False):
        #     return result
        # s = json.dumps(d)
        # return Result(True), s

    @classmethod
    def from_json(cls, data):
        return cls.from_dict(json.loads(data))
    
    @abstractclassmethod
    def from_dict(cls, data) -> Tuple[Result, Dict]:
        raise NotImplementedError()
