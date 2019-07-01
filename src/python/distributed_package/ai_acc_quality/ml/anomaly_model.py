"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from azureml.core.workspace import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model
from numpy import matrix
from typing import List, Tuple
import json
import os
from os import walk
import shutil
import pickle
from ai_acc_quality.result import Result, Error
from ai_acc_quality.data_models.telemetry import Telemetry
from ai_acc_quality.data_models.widget import Widget, Widget_Classification

class Anomaly_Model():
    """
    Class representing the anomaly ML model
    """
    model = None #hydrated model
    _model_name = "Anomoly"
    _x_transform = None
    _y_transform = None
    serial_number = None
    
    def __init__(self, serial_number):
        self.serial_number = serial_number

    def model_diagnostics(self):
        return self.serial_number

    def _resolve_model_tags(self):
        return {"serial_number" : self.serial_number}

    def _get_az_ml_ws(self, az_sub_id : str, az_rg : str, 
                    az_ml_ws_name : str, az_sp_ten_id : str,
                    az_sp_app_id : str, az_sp_pass : str) -> Tuple[Result, Workspace]:
        """
        Returns a workspace for azure ml
        """
        az_ml_ws = None
        try: #Authenticate w/ AZ ML & Get Workspace
            az_sp = ServicePrincipalAuthentication(az_sp_ten_id, az_sp_app_id, az_sp_pass)
            az_ml_ws = Workspace(az_sub_id, az_rg, az_ml_ws_name, auth=az_sp)
        except Exception as e:
            return Result(False, 
                        Error("1004", #Unable to authenticate
                        additional_info=self.model_diagnostics() + str(e))), None
        return Result(True), az_ml_ws

    def load_model(self, az_sub_id : str, az_rg : str, 
                    az_ml_ws_name : str, az_sp_ten_id : str,
                    az_sp_app_id : str, az_sp_pass : str) -> Result:
        """
        Loads the specified machine learning model
        """
        result, ws = self._get_az_ml_ws(az_sub_id, az_rg, az_ml_ws_name, az_sp_ten_id, az_sp_app_id, az_sp_pass)
        if(result.success is False):
            return result

        try: #Query for & Download Model
            model = Model(ws, name=self._model_name, tags=self._resolve_model_tags)
            model.download("./assets/")
            #TODO: remove workaround for ml sdk dropping assets into /assets/user folder when files dropped to consistent location
            for dir_p, _, f_n in walk("./assets"):
                for f in f_n:
                    abs_path = os.path.abspath(os.path.join(dir_p, f))
                    shutil.move(abs_path, "./assets/" + f)
        except Exception as e:
            return Result(False, 
            Error("1001", #Model does not exist
            additional_info=self.model_diagnostics() + str(e)))

        try: #Hydrate this object from downloaded model files
            self.model = pickle.load("./assets/model.pkl")
            self._x_transform = pickle.load("./assets/x_transform.pkl")
            self._y_transform = pickle.load("./assets/y_transform.pkl")
        except Exception as e:
            return Result(False, 
            Error("1005", #Model Files don't exist
            additional_info=self.model_diagnostics() + str(e)))
        return Result(True)

    def register_model(self, model_files_root : str,
                        az_sub_id : str, az_rg : str, 
                        az_ml_ws_name : str, az_sp_ten_id : str,
                        az_sp_app_id : str, az_sp_pass : str) -> Result:
        """
        Registers the model with the AZML Service
        """
        result, ws = self._get_az_ml_ws(az_sub_id, az_rg, az_ml_ws_name, az_sp_ten_id, az_sp_app_id, az_sp_pass)
        if(result.success is False):
            return result
        try:
            Model.register(ws, model_path = model_files_root, model_name = self._model_name,
                            tags = self._resolve_model_tags())
        except Exception as e:
            return Result(False, error=Error("1006", additional_info=self.model_diagnostics() + str(e)))
        return Result(True)


    def _pre_process_data(self, welds : List[Telemetry]) -> Tuple[Result, matrix]:
        """
        transforms a list of telemetry into the required multi-dimensional matrix for input to the prediction algorithm
        """
        err = Error(code = "2001") #not implemented
        res = Result(False, error=err)
        return res

    def _post_process_data(self, raw_prediction : float) -> Tuple[Result, Widget_Classification]:
        """
        takes raw output and creates a widget classification
        """
        err = Error(code = "2001") #not implemented
        res = Result(False, error=err)
        return res

    def classify(self, widget : Widget) -> Tuple[Result, Widget]:
        """
        takes a widget and returns a widget with a populated classification object
        """
        err = Error(code = "2001") #not implemented
        res = Result(False, error=err)
        return res, None
