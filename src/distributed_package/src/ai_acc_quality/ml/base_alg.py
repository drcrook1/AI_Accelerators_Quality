"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from abc import ABC, abstractclassmethod
from typing import Dict, Tuple
import json

class Base_Alg(ABC):
    """
    Base Algorithm, ALL Algorithms should inherit from this.
    """
    
    @abstractclassmethod
    def load_model(self):
        """
        This should hydrate all required model files such that predict can work.
        """
        raise NotImplementedError()
    
    @staticmethod
    def predict(self, data):
        """
        Predict should cover pre-processing, predicting and post processing
        """
        raise NotADirectoryError()