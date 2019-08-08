import json
import logging
import os
import random
import tempfile
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
from azureml.core.authentication import MsiAuthentication
from azureml.core.model import Model
from azureml.core.workspace import Workspace
from joblib import load
from torch.utils.data import DataLoader

from ai_acc_quality.data_models.widget import Widget, Widget_Classification
from ai_acc_quality.ml.score import score


class MLModelClient:

    def __init__(self):
        pass

    def azureMLAuthentication(self):
        return MsiAuthentication()

    def azureMLWorkspace(self):
        return Workspace(
            subscription_id=os.environ["AzureMLSubscriptionId"],
            resource_group=os.environ["AzureMLResourceGroup"],
            workspace_name=os.environ["AzureMLWorkspace"],
            auth=self.azureMLAuthentication())

    def _downloadModel(self, ws, modelName, dirName):
        model = Model(ws, name=modelName)
        model.download(target_dir=dirName)

    def classify_widget(self, w: Widget):
        ws = self.azureMLWorkspace()

        # Get & Download model
        with tempfile.TemporaryDirectory() as tmpdir:
            self._downloadModel(ws, "sklearn_preprocessing", tmpdir)
            self._downloadModel(ws, "autoencoder", tmpdir)
            self._downloadModel(ws, "autoencoder_stats", tmpdir)

            return score(tmpdir, w)
