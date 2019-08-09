import json
import os
from datetime import datetime

import joblib
import numpy as np
import torch
from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from ai_acc_quality.ml.anomaly import score_anomaly
from ai_acc_quality.ml.preprocessing import score_preprocessing


def score(modelPath:str, widget:Widget) -> Widget_Classification:
    
    preprocessing = joblib.load(os.path.join(modelPath, "preprocessing.joblib"))
    anomaly_model = torch.load(os.path.join(modelPath, "model.pt"))
    output1 = score_preprocessing(preprocessing, widget)
    output2 = score_anomaly(anomaly_model, output1)
    with open(os.path.join(modelPath, "model_stats.json")) as statsf:
        model_stats = json.load(statsf)
    mean = model_stats['mean']
    stdev = model_stats['stdev']

    c = Widget_Classification()
    c.classified_time = datetime.utcnow()
    c.mean = mean
    c.std = stdev
    c.std_dist = (output2.item() - mean) / stdev
    c.threshold = 3
    return c
