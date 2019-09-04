"""
Author: David Crook
Email: DaCrook@Microsoft.com
"""
from ai_acc_quality.ml.base_alg import Base_Alg
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
import random
from datetime import datetime
from keras.models import load_model
import pickle
import numpy as np
import os

class WidgetClassifier(Base_Alg):
    """
    ML Class that performs actual predictions.
    """
    encoder = None
    cluster = None
    anomaly_definition = None
    telemetry_keys = None
    feature_keys = None
    unique_features = None

    def get_model_assets_location(self):
        path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(path, "ml_assets/anomaly")

    def load_model(self):
        prefix = self.get_model_assets_location()
        self.encoder = load_model(os.path.join(prefix, "anomaly_encoder.h5"))
        self.cluster = pickle.load(open(os.path.join(prefix, "clustering_model.pkl"), "rb"))
        self.anomaly_definition = pickle.load(open(os.path.join(prefix, "anomaly_definition.pkl"), "rb"))
        self.telemetry_keys = pickle.load(open(os.path.join(prefix, "telemetry_keys.pkl"), "rb"))
        self.telemetry_keys.sort()
        return True

    def pre_process(self, data : Widget) -> np.array:
        telemetry = data.to_dict()[1]["telemetry"]
        telemetry = sorted(telemetry, key = lambda i: i["time_stamp"])
        n_steps = len(telemetry)
        n_vars = len(self.telemetry_keys)
        tel_data = np.empty((n_steps, n_vars))
        for i in range(0,n_steps):
            for j in range(0,n_vars):
                tel_data[i,j] = float(telemetry[i][self.telemetry_keys[j]])
        return tel_data.reshape(1,n_steps,n_vars)


    def predict(self, data : Widget) -> Widget_Classification:
        wc = Widget_Classification()
        processed = self.pre_process(data)
        feature_map = self.encoder.predict(processed)
        cluster_assignment = self.cluster.predict(feature_map)
        if(cluster_assignment == self.anomaly_definition["anomaly"]):
            wc.is_good = False
            #wc.std_dist = 4
            #wc.std = 5
        else:
            wc.is_good = True
            #wc.std_dist = 0.5
            #wc.std = 5
        wc.classified_time = datetime.utcnow()
        #wc.threshold = 3
        #wc.mean = 1
        return wc
