# storage account name "[concat(toLower(parameters('baseName')), 'amlsa')]" = dacrookamlsa
param(
    [string]$pypiurl = "None",
    [string]$pypipackagename = "None"
)

$basename = "aiquadev"
$resourceGroupName = "ai-quality-dev" 
$location = "eastus"
$storage_aml = $basename + "amlsa"
$aml_ws_name = $basename + "-AML-WS"


$storage_key = ([string](az storage account keys list -g $resourceGroupName -n $storage_aml | ConvertFrom-Json)[0].value

#
# Inject Custom Image to Run Configuration for Inference Pipeline
#
cd ../src/anomaly_auto_cluster/src/train

((Get-Content -path base_conda_dependencies.yml -Raw) -replace '{{#PACKAGE_URL#}}',$pypiurl) | Set-Content -Path conda_dependencies.yml
((Get-Content -path conda_dependencies.yml -Raw) -replace '{{#PACKAGE_NAME#}}',$pypipackagename) | Set-Content -Path conda_dependencies.yml

cd ../../../../deploy

az ml datastore attach-blob -n "rawstore" -a $storage_aml -c "rawdata" -w $aml_ws_name --resource-group $resourceGroupName -k $storage_key
az ml datastore attach-blob -n "processedstore" -a $storage_aml -c "processeddata" -w $aml_ws_name --resource-group $resourceGroupName -k $storage_key
az ml datastore attach-blob -n "modelstore" -a $storage_aml -c "modelstore" -w $aml_ws_name --resource-group $resourceGroupName -k $storage_key
$result_pipeline_create = az ml pipeline create -n "anomaly_train_auto_cluster" -y "ml_pipelines/auto_cluster_train.yml" -w $aml_ws_name --resource-group $resourceGroupName

Write-Host "Pipeline Endpoint: '$result_pipeline_create'";