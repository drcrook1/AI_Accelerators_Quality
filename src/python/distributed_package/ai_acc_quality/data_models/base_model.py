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

    @abstractclassmethod
    def to_json(self) -> Tuple[Result, str]:
        raise NotImplementedError()
