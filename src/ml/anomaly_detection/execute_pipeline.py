import azureml.core
from azureml.core import Workspace, Experiment
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.compute import ComputeTarget, DatabricksCompute
from azureml.exceptions import ComputeTargetException
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline
import os

db_compute_name = os.environ["DB_COMPUTE_NAME"]
db_workspace_name = os.environ["DB_WORKSPACE_NAME"]
db_rg = os.environ["RESOURCE_GROUP"]
db_access_token = os.environ["DB_ACCESS_TOKEN"]
az_ml_ws_name = os.environ["AZ_ML_WS_NAME"]

def get_workspace() -> Workspace:
    tenant_id = os.environ["SP_TENANT_ID"]
    app_id = os.environ["SP_APP_ID"]
    secret = os.environ["SP_PASSWORD"]
    sub_id = os.environ["SUBSCRIPTION"]
    sp = ServicePrincipalAuthentication(tenant_id, app_id, secret)
    ws = Workspace(sub_id, db_rg, az_ml_ws_name, auth=sp)
    return ws

def get_db_compute(ws:Workspace) -> DatabricksCompute:
    db_compute = None
    try:
        db_compute = ComputeTarget(ws, db_compute_name)
    except ComputeTargetException:
        attach_config = DatabricksCompute.attach_configuration(
            resource_group=db_rg,
            workspace_name=db_workspace_name,
            access_token=db_access_token
        )
        db_compute = ComputeTarget.attach(ws, db_compute_name, attach_config)
        db_compute.wait_for_completion(True)
    return db_compute

ws = get_workspace()
db_compute = get_db_compute(ws)

train_step = PythonScriptStep(
    script_name = "train.py",
    compute_target=db_compute,
    source_directory="./notebooks",
    num_workers=4
)

steps = [train_step]
pipeline = Pipeline(workspace=ws, steps=steps)
run = Experiment(ws, "anomaly_detector").submit(pipeline)
run.wait_for_completion()