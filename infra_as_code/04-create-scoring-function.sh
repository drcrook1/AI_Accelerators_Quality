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
setting_template="$PROC_FUNCTION_DIR/local.settings.sample.json"
setting_out="$PROC_FUNCTION_DIR/local.settings.json"
if [ -e "$setting_out" ]; then
	setting_template="$setting_out"
fi
jq ".Values.EventHubsConnectionString = \"$EVENTHUB_CS\"" $setting_template > $setting_out.tmp
mv $setting_out.tmp $setting_out

echo 'publishing app'
(cd "$PROC_FUNCTION_DIR" && func azure functionapp publish "$PROC_FUNCTION_APP_NAME" --publish-local-settings --overwrite-settings)
