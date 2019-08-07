import json
import os

import joblib
import numpy as np
import torch

from ai_acc_quality.data_models.widget import Widget
from ai_acc_quality.ml.anomaly import score_anomaly
from ai_acc_quality.ml.preprocessing import score_preprocessing


def score(modelPath:str, widget:Widget):
    preprocessing = joblib.load(modelPath + "/preprocessing.joblib")
    anomaly_model = torch.load(modelPath + "/model.pt")
    output1 = score_preprocessing(preprocessing, widget)
    output2 = score_anomaly(anomaly_model, output1)
    with open(os.path.join(modelPath, "model_stats.json")) as statsf:
        model_stats = json.load(statsf)
    mean = model_stats['mean']
    stdev = model_stats['stdev']
    return {
        "score": output2,
        "std_dist": ((output2 - mean) / stdev),
        "std": stdev,
        "mean": mean,
        "threshold": mean + 3 * stdev,
    }
