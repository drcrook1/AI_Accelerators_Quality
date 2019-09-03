from azureml.core.workspace import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model as azModel
import os
import shutil
import argparse

try:
    sub_id = os.environ["SUBSCRIPTION_ID"]
    rg = os.environ["RESOURCE_GROUP"]
    ml_ws_name = os.environ["ML_WS_NAME"]
except Exception:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sub_id")
    parser.add_argument("--rg")
    parser.add_argument("--ml_ws_name")
    args = parser.parse_args()
    sub_id = args.sub_id
    rg = args.rg
    ml_ws_name = args.ml_ws_name

az_ws = Workspace(sub_id, rg, ml_ws_name)

prefix = "./ProcessTelemetry/ml_assets/"

if not os.path.exists(prefix):
    os.makedirs(prefix)
else:
    shutil.rmtree(prefix)
    os.makedirs(prefix, exist_ok=True)

azml_model = azModel(az_ws, name="anomaly_enc_dec")
azml_model.download(target_dir=prefix)