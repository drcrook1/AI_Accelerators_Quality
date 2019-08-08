"""
Author: Alexandre Gattiker
Handle: https://github.com/algattik
"""
from locust import HttpLocust, TaskSet, task
import os
import random
import requests
import datetime, time
import uuid
import sys    
import urllib
from urllib.parse import quote, quote_plus
import hmac
import hashlib
import base64
import json

from ai_acc_quality.data_models.widget import Widget
from ai_acc_quality.data_models.telemetry import Telemetry

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_auth_token(eh_namespace, eh_name, eh_key):
    uri = quote_plus("https://{0}.servicebus.windows.net/{1}".format(eh_namespace, eh_name))
    eh_key = eh_key.encode('utf-8')
    expiry = str(int(time.time() + 60 * 60 * 24 * 31))
    string_to_sign = (uri + '\n' + expiry).encode('utf-8')
    signed_hmac_sha256 = hmac.HMAC(eh_key, string_to_sign, hashlib.sha256)
    signature = quote(base64.b64encode(signed_hmac_sha256.digest()))
    return 'SharedAccessSignature sr={0}&sig={1}&se={2}&skn={3}'.format(uri, signature, expiry, "RootManageSharedAccessKey")

EVENT_HUB = {
    'namespace': os.environ['EVENTHUB_NAMESPACE'],
    'name': os.environ['EVENTHUB_NAME'],
    'key': os.environ['EVENTHUB_KEY'],
    'token': get_auth_token(os.environ['EVENTHUB_NAMESPACE'], os.environ['EVENTHUB_NAME'], os.environ['EVENTHUB_KEY'])
}

class DeviceSimulator(TaskSet):
    headers = {
        'Content-Type': 'application/atom+xml;type=noretry;charset=utf-8 ',
        'Authorization': EVENT_HUB['token'],
        'Host': EVENT_HUB['namespace'] + '.servicebus.windows.net'
    }

    endpoint = "/" + EVENT_HUB['name'] + "/messages?timeout=60&api-version=2014-01"

    @task
    def sendData(self):

        factoryId = 'factory-{0}'.format(random.randint(0, 999))

        t = Telemetry()
        t.voltage = random.uniform(10,100)
        t.amperage = random.uniform(10,100)
        t.ambient_temp = random.uniform(10,100)
        t.ambient_humidity = random.uniform(10,100)
        t.flux_capacitance = random.uniform(10,100)
        t.time_stamp = datetime.datetime.utcnow()

        w = Widget()
        w.serial_number = uuid.uuid4().hex
        w.factory_id = factoryId
        w.line_id = random.choice(["L1", "L2", "L3"])
        w.telemetry = [t]
        w_json = w.to_json()

        headers = dict(self.headers)
        brokerProperties = { 'PartitionKey': factoryId }
        headers["BrokerProperties"] = json.dumps(brokerProperties)
        self.client.post(self.endpoint, data=w_json, verify=False, headers=headers)

class MyLocust(HttpLocust):
    task_set = DeviceSimulator
    min_wait = 250
    max_wait = 500
