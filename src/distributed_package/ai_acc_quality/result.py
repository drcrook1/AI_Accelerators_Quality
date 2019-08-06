'''
Author: David Crook
Email: DaCrook@Microsoft.com

Basic Results object for ALL processing
'''
import json

POSSIBLE_ERRORS = {
    "1001" : {"code" : "1001", "code_family" : "ML", "message" : "MODEL DOES NOT EXIST"},
    "1002" : {"code" : "1002", "code_family" : "ML", "message" : "NOT ENOUGH DATA TO PREDICT"},
    "1004" : {"code" : "1004", "code_family" : "ML", "message" : "UNABLE TO AUTHENTICATE WITH AZ ML SERVICE"},
    "1005" : {"code" : "1005", "code_family" : "ML", "message" : "EXPECTED MODEL FILES DO NOT EXIST"},
    "1006" : {"code" : "1006", "code_family" : "ML", "message" : "FAILED TO REGISTER MODEL"},
    "2001" : {"code" : "2001", "code_family" : "SYSTEM", "message" : "FUNCTION NOT IMPLEMENTED YET"},
    "2002" : {"code" : "2002", "code_family" : "SYSTEM", "message" : "UNKNOWN SYSTEM ERROR"}
    }

class Error():
    message : str = None
    code : int = None 
    code_family : str = None

    def __init__(self, code:str, code_family:str = None, message:str = None, additional_info:str = None):
        try:
            err = POSSIBLE_ERRORS[code]
            self.code = code
            self.code_family = err["code_family"]
            self.message = err["message"]
        except Exception:
            self.code = code
            self.code_family = code_family
            self.message = message
        if(additional_info is not None):
            self.message = self.message + "-" + additional_info

    def to_dict(self):
        r = {}
        r["code"] = self.code
        r["message"] = self.message
        return r

    def to_log_message(self):
        """
        use this for logging functions
        """
        msg = "{}-{}-{}".format(self.code_family, self.code, self.message)
        return msg
    
    def to_json(self):
        d = self.to_dict()
        return json.dumps(d)

class Result():
    success : bool = None 
    message : str = None 
    error : Error = None 

    def __init__(self, success:bool, message:str = None, error:Error = None):
        self.success = success
        self.message = message
        self.error = error

    def to_dict(self):
        r = {}
        r["success"] = self.success
        r["message"] = self.message
        return r
    
    def to_json(self):
        d = self.to_dict()
        return json.dumps(d)