#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}
EVENTHUB_NAMESPACE=${EVENTHUB_NAMESPACE:-${PREFIX}ehubs}
WEB_APP_NAME=${WEB_APP_NAME:-${PREFIX}"web"}
PROC_FUNCTION_PLAN_NAME=${PROC_FUNCTION_APP_NAME:-${PREFIX}"plan"}
PROC_FUNCTION_APP_NAME=${PROC_FUNCTION_APP_NAME:-${PREFIX}"process"}
PROC_FUNCTION_SKU=${PROC_FUNCTION_SKU:-S1}
PROC_FUNCTION_WORKERS=${PROC_FUNCTION_WORKERS:-1}
SQL_SERVER_NAME=${SQL_SERVER_NAME:-${PREFIX}sql}
SQL_DATABASE_NAME=${SQL_DATABASE_NAME:-${PREFIX}db}
SQL_ADMIN_USER=${SQL_ADMIN_USER:-serveradmin}
SQL_ADMIN_PASS=${SQL_ADMIN_PASS}
STORAGE_TABLE_NAME=${STORAGE_TABLE_NAME:-Predictions}

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
    -o none

echo 'getting connection strings'
eventhubs_cs=$(az eventhubs namespace authorization-rule keys list -g $RESOURCE_GROUP --namespace-name $EVENTHUB_NAMESPACE --name RootManageSharedAccessKey --query "primaryConnectionString" -o tsv)
sql_cs="Driver={ODBC Driver 17 for SQL Server};Server=tcp:$SQL_SERVER_NAME.database.windows.net;Database=$SQL_DATABASE_NAME;Uid=$SQL_ADMIN_USER;Pwd=$SQL_ADMIN_PASS;Encrypt=yes;TrustServerCertificate=no;"
storage_cs="DefaultEndpointsProtocol=https;AccountName=$AZURE_STORAGE_ACCOUNT;AccountKey=$(az storage account keys list -g $RESOURCE_GROUP -n $AZURE_STORAGE_ACCOUNT -o tsv --query "[0].value");EndpointSuffix=core.windows.net"
webapp_url="https://$(az webapp show -g $RESOURCE_GROUP -n $WEB_APP_NAME | jq -r .defaultHostName)"

echo 'adding app settings for connection strings'

az functionapp config appsettings set --name $PROC_FUNCTION_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
      EventHubsConnectionString="$eventhubs_cs" \
      SqlDatabaseConnectionString="$sql_cs" \
      TableStorageConnectionString="$storage_cs" \
      ModelsStorageConnectionString="$storage_cs" \
      SignalIOServerHttpEndpoint="$webapp_url" \
    -o none
