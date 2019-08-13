"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.result import Error, Result

class TestResultsAndErrors(object):
    """
    Test Suite against Results and Errors Objects
    """

    def test_result_with_error(self):
        """
        Test results and error objects
        """
        err = Error("1001")
        assert(err.code_family == "ML")
        res = Result(False, error=err)
        assert(res.error is not None)
    
    
    def test_log_msg_format_error(self):
        err = Error("1001")
        msg = err.to_log_message()
        assert("ML-1001-MODEL DOES NOT EXIST" == msg)