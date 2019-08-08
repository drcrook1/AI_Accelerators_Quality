import argparse
import os

from azureml.core import Datastore, Experiment, Workspace
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.compute_target import ComputeTargetException
from azureml.data.data_reference import DataReference
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import EstimatorStep
from azureml.train.dnn import PyTorch
from azureml.train.sklearn import SKLearn
import sklearn

# get command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--subscription_id', type=str, required=True, help='subscription ID')
parser.add_argument('--resource_group', type=str, required=True, help='resource group')
parser.add_argument('--workspace', type=str, required=True, help='Azure ML workspace name')
parser.add_argument('--experiment', type=str, default='ai_quality', help='Azure ML experiment name')
parser.add_argument('--storage_account', type=str, required=True, help='Storage account name')
parser.add_argument('--storage_container', type=str, default='eventhubs', help='Storage container name')
parser.add_argument('--storage_key', type=str, required=True, help='Storage account key')
parser.add_argument('--storage_path', type=str, required=True, help='Path to Avro data in storage container')
args = parser.parse_args()

ws = Workspace(
    subscription_id = args.subscription_id,
    resource_group = args.resource_group,
    workspace_name = args.workspace
    )

# Choose a name for your CPU cluster
cpu_cluster_name = "cpu4"

# Verify that cluster does not exist already
try:
    cpu_cluster = ComputeTarget(workspace=ws, name=cpu_cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    ssh_key = None
    try:
        with open(os.path.expanduser("~/.ssh/id_rsa.pub")) as fp:
            ssh_key = fp.read()
    except IOError:
        pass

    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',
                                                           min_nodes=0,
                                                           max_nodes=3,
                                                           idle_seconds_before_scaledown=1200,
                                                           admin_username=os.getenv('USER'),
                                                           admin_user_ssh_key=ssh_key,
                                                           )
    cpu_cluster = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

cpu_cluster.wait_for_completion(show_output=True)

old_datastore = [ds for ds in ws.datastores if ds=="telemetry"]
if old_datastore:
   old_ds = Datastore.get(ws, "telemetry")
   old_ds.unregister()

telemetry_ds = Datastore.register_azure_blob_container(workspace=ws, 
                                                    datastore_name='telemetry', 
                                                    container_name=args.storage_container,
                                                    account_name=args.storage_account,
                                                    account_key=args.storage_key,
                                                    )

input_data = DataReference(
    datastore=telemetry_ds,
    data_reference_name="input_data",
    path_on_datastore=args.storage_path,
    )


preprocessing_est = SKLearn(source_directory='.', 
                    compute_target=cpu_cluster,
                    entry_script='train_dataprep.py',
                    pip_packages=['fastavro'],
                    framework_version=sklearn.__version__,
                   )

output = PipelineData("output", datastore=telemetry_ds)
preprocessing_step = EstimatorStep(name="Preprocessing_Train", 
                         estimator=preprocessing_est, 
                         estimator_entry_script_arguments=["--data_dir", input_data, "--output_data_dir", output],
                         inputs=[input_data], 
                         outputs=[output], 
                         compute_target=cpu_cluster,
                         allow_reuse=True,
                         )


pytorch_est = PyTorch(source_directory='.', 
                    compute_target=cpu_cluster,
                    entry_script='train_pytorch.py',
                    use_gpu=False,
                    framework_version='1.1',
                    )

pytorch_step = EstimatorStep(name="PyTorch_Train", 
                         estimator=pytorch_est, 
                         estimator_entry_script_arguments=["--data_dir", output],
                         inputs=[output], 
                         compute_target=cpu_cluster,
                         allow_reuse=True,
                         )


pipeline = Pipeline(workspace=ws, steps=[preprocessing_step, pytorch_step])
run = Experiment(ws, args.experiment).submit(pipeline)
run.wait_for_completion(show_output=True)

preprocessing_run = next(step for step in run.get_steps() if step.name=="Preprocessing_Train")
pytorch_run = next(step for step in run.get_steps() if step.name=="PyTorch_Train")

print("Registering models...")
preprocessing_model = preprocessing_run.register_model(model_name='sklearn_preprocessing', model_path='outputs/preprocessing.joblib')
print(preprocessing_model.name, preprocessing_model.id, preprocessing_model.version, sep='\t')

pytorch_model = pytorch_run.register_model(model_name='autoencoder', model_path='outputs/model.pt')
print(pytorch_model.name, pytorch_model.id, pytorch_model.version, sep='\t')
