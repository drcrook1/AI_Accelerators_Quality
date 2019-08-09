import copy
import logging

import requests
from ai_acc_quality.data_models.widget import Widget


class WidgetWebAppClient:

    def __init__(self, requests_obj, baseURL):
        self.requests_obj = requests_obj
        self.baseURL = baseURL

    def post(self, widget):

        w = copy.deepcopy(widget)
        # Warning: has side-effect to clear telemetry list, ust be last action in function
        w.telemetry.clear()

        good = w.classification.is_good()
        endpoint = "goodwidget" if good else "badwidget"
        headers = {'Content-type': 'application/json'}
        endpoint_url = "{}/api/v1/live/{}".format(self.baseURL, endpoint)
        try:
            r:requests.Response = self.requests_obj.post(endpoint_url, data=w.to_json(), headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.exception(e)
