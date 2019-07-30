#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}
EVENTHUB_NAMESPACE=${EVENTHUB_NAMESPACE:-${PREFIX}ehubs}
PROC_FUNCTION_PLAN_NAME=${PROC_FUNCTION_APP_NAME:-${PREFIX}"plan"}
PROC_FUNCTION_APP_NAME=${PROC_FUNCTION_APP_NAME:-${PREFIX}"process"}
PROC_FUNCTION_SKU=${PROC_FUNCTION_SKU:-S2}
PROC_FUNCTION_WORKERS=${PROC_FUNCTION_WORKERS:-1}

echo 'creating app service plan'
echo ". name: $PROC_FUNCTION_PLAN_NAME"
#'if' is a workaround for https://github.com/Azure/azure-cli/issues/9833
if [ -z "$(az appservice plan show -g $RESOURCE_GROUP -n $PROC_FUNCTION_PLAN_NAME)" ]; then
  az appservice plan create -g $RESOURCE_GROUP -n $PROC_FUNCTION_PLAN_NAME \
    --is-linux \
    --number-of-workers $PROC_FUNCTION_WORKERS --sku $PROC_FUNCTION_SKU \
    -o tsv
fi

echo 'creating function app'
echo ". name: $PROC_FUNCTION_APP_NAME"
az functionapp create -g $RESOURCE_GROUP -n $PROC_FUNCTION_APP_NAME \
    --plan $PROC_FUNCTION_PLAN_NAME \
    --os-type Linux --runtime python \
    --storage-account $AZURE_STORAGE_ACCOUNT \
    -o tsv

echo 'getting shared access key'
EVENTHUB_CS=`az eventhubs namespace authorization-rule keys list -g $RESOURCE_GROUP --namespace-name $EVENTHUB_NAMESPACE --name RootManageSharedAccessKey --query "primaryConnectionString" -o tsv`
 
echo 'adding app settings for connection strings'

echo ". EventHubsConnectionString"
az functionapp config appsettings set --name $PROC_FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings EventHubsConnectionString=$EVENTHUB_CS \
    -o tsv
