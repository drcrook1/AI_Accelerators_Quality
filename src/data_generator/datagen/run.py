#!/bin/env python
"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""
import datagen.helpers as helpers
import time

if __name__ == "__main__":
    while(True):
        hub, sender = helpers.get_event_hub()
        hub.run()
        widgets = []
        widgets.append(helpers.generate_widget(is_anomaly=True))
        for i in range(0,100):
            widgets.append(helpers.generate_widget())
        res = helpers.push_to_event_hub(sender, widgets, sleep=1)
        if(res is True):
            print("pushed 10 normal & 1 anomaly")
        time.sleep(3)