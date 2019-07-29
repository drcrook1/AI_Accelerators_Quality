#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

PLAN_NAME=$PROC_FUNCTION_APP_NAME"plan"

echo 'creating app service plan'
echo ". name: $PLAN_NAME"
#'if' is a workaround for https://github.com/Azure/azure-cli/issues/9833
set -x
if [ -z "$(az appservice plan show -g $RESOURCE_GROUP -n $PLAN_NAME)" ]; then
  az appservice plan create -g $RESOURCE_GROUP -n $PLAN_NAME \
    --is-linux \
    --number-of-workers $PROC_FUNCTION_WORKERS --sku $PROC_FUNCTION_SKU --location $LOCATION \
    -o tsv >> log.txt
fi

echo 'creating function app'
echo ". name: $PROC_FUNCTION_APP_NAME"
az functionapp create -g $RESOURCE_GROUP -n $PROC_FUNCTION_APP_NAME \
    --plan $PLAN_NAME \
    --os-type Linux --runtime python \
    --storage-account $AZURE_STORAGE_ACCOUNT \
    -o tsv >> log.txt

echo 'getting shared access key'
EVENTHUB_CS=`az eventhubs namespace authorization-rule keys list -g $RESOURCE_GROUP --namespace-name $EVENTHUB_NAMESPACE --name RootManageSharedAccessKey --query "primaryConnectionString" -o tsv`
 
echo 'adding app settings for connection strings'

echo ". EventHubsConnectionString"
az functionapp config appsettings set --name $PROC_FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings EventHubsConnectionString=$EVENTHUB_CS \
    -o tsv >> log.txt

echo 'publishing app'
(
cd ../src/python/inference_function
export PIP_FIND_LINKS=../distributed_package/dist/
test -d $PIP_FIND_LINKS || (echo "Can't find $PWD/$PIP_FIND_LINKS. Have you run setup.py? E.g. 'python3 setup.py --version 0.0.0 sdist bdist_wheel'"; exit 1)
test -f local.settings.json || cp local.settings.sample.json local.settings.json 
PIP_FIND_LINKS=../distributed_package/dist/ func azure functionapp publish "$PROC_FUNCTION_APP_NAME"
)
