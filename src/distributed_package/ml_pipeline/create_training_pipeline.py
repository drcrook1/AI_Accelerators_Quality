import argparse
import os

import sklearn
from azureml.core import Datastore, Experiment, Workspace
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.compute_target import ComputeTargetException
from azureml.data.data_reference import DataReference
from azureml.pipeline.core import Pipeline, PipelineData, PipelineParameter
from azureml.pipeline.steps import EstimatorStep, PythonScriptStep
from azureml.train.dnn import PyTorch
from azureml.train.sklearn import SKLearn

# get command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--subscription_id', type=str,
                    required=True, help='subscription ID')
parser.add_argument('--resource_group', type=str,
                    required=True, help='resource group')
parser.add_argument('--workspace', type=str, required=True,
                    help='Azure ML workspace name')
parser.add_argument('--storage_account', type=str,
                    required=True, help='Storage account name')
parser.add_argument('--storage_container', type=str,
                    default='eventhubs', help='Storage container name for telemetry data')
parser.add_argument('--storage_key', type=str,
                    required=True, help='Storage account key')
parser.add_argument('--storage_path', type=str, required=True,
                    help='Path to Avro data in storage container')
parser.add_argument('--out_pipeline_id', type=str,
                    default='pipeline_id.txt', help='File to write created Pipeline ID into')
parser.add_argument('--run_experiment', type=str,
                    help='Run pipeline after creation. Provide experiment name as argument')
args = parser.parse_args()

ws = Workspace(
    subscription_id=args.subscription_id,
    resource_group=args.resource_group,
    workspace_name=args.workspace
)

# Choose a name for your CPU cluster
cpu_cluster_name = "cpu1"

# Verify that cluster does not exist already
try:
    cpu_cluster = ComputeTarget(workspace=ws, name=cpu_cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    compute_config = AmlCompute.provisioning_configuration(
        vm_size='STANDARD_D2_V2',
        min_nodes=0,
        max_nodes=3,
        idle_seconds_before_scaledown=1200,
    )
    cpu_cluster = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

cpu_cluster.wait_for_completion(show_output=True)

old_telemetry_ds = [ds for ds in ws.datastores if ds == "telemetry"]
if old_telemetry_ds:
    telemetry_ds = Datastore.get(ws, 'telemetry')
else:
    telemetry_ds = Datastore.register_azure_blob_container(
        workspace=ws,
        datastore_name='telemetry',
        container_name=args.storage_container_telemetry,
        account_name=args.storage_account,
        account_key=args.storage_key,
    )

input_data = DataReference(
    datastore=telemetry_ds,
    data_reference_name="input_data",
    path_on_datastore=args.storage_path,
)

preprocessing_est = SKLearn(
    source_directory='src',
    compute_target=cpu_cluster,
    entry_script='train_dataprep.py',
    pip_packages=['fastavro'],
    framework_version=sklearn.__version__,
)

preprocessed_data = PipelineData("preprocessed_data")
preprocessing_model = PipelineData("preprocessing_model")
preprocessing_step = EstimatorStep(
    name="Preprocessing_Train",
    estimator=preprocessing_est,
    estimator_entry_script_arguments=[
        "--data_dir", input_data,
        "--output_model_dir", preprocessing_model,
        "--output_data_dir", preprocessed_data,
    ],
    inputs=[input_data],
    outputs=[preprocessed_data, preprocessing_model],
    compute_target=cpu_cluster,
    allow_reuse=True,
)

pytorch_est = PyTorch(
    source_directory='src',
    compute_target=cpu_cluster,
    entry_script='train_pytorch.py',
    use_gpu=False,
    framework_version='1.1',
)

anomaly_model = PipelineData("anomaly_model")
model_name = PipelineParameter(name="model_name", default_value='anomaly')
pytorch_step = EstimatorStep(
    name="PyTorch_Train",
    estimator=pytorch_est,
    estimator_entry_script_arguments=[
        "--data_dir", preprocessed_data,
        "--output_dir", anomaly_model,
        "--num_epochs", 2,
    ],
    inputs=[preprocessed_data],
    outputs=[anomaly_model],
    compute_target=cpu_cluster,
    allow_reuse=True,
)

register = PythonScriptStep(
    name="Register model for deployment",
    source_directory='ml_pipeline',
    script_name="register_models.py",
    inputs=[preprocessing_model, anomaly_model],
    arguments=[
        '--model_name', model_name,
        '--model_assets_path', preprocessing_model, anomaly_model,
    ],
    compute_target=cpu_cluster,
)

pipeline = Pipeline(workspace=ws, steps=[
                    preprocessing_step, pytorch_step, register])
pipeline.validate()

mlpipeline = pipeline.publish(name="Anomaly Detection Training Pipeline",
                              description="Retrain an anomaly detection model")

with open(args.out_pipeline_id, "w") as op:
    op.write("{}\n".format(mlpipeline.id))

print("Pipeline created.")

if args.run_experiment:
    run = Experiment(ws, args.run_experiment).submit(pipeline)
    run.wait_for_completion(show_output=True)
else:
    print("You can run the pipeline with:")
    print("  az ml run submit-pipeline -g {} -w {} -n anomaly_train -i $(cat {})".format(
        args.resource_group, args.workspace, args.out_pipeline_id))
