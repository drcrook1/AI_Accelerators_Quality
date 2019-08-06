#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}
WEB_APP_PLAN_NAME=${WEB_APP_NAME:-${PREFIX}"webplan"}
WEB_APP_NAME=${WEB_APP_NAME:-${PREFIX}"web"}
WEB_APP_SKU=${WEB_APP_SKU:-S2}
WEB_APP_WORKERS=${WEB_APP_WORKERS:-1}
WEB_APP_DUMMY_CONTAINER=${WEB_APP_DUMMY_CONTAINER:-nginx}
SQL_SERVER_NAME=${SQL_SERVER_NAME:-${PREFIX}sql}
SQL_DATABASE_NAME=${SQL_DATABASE_NAME:-${PREFIX}db}
SQL_ADMIN_USER=${SQL_ADMIN_USER:-serveradmin}
SQL_ADMIN_PASS=${SQL_ADMIN_PASS}
STORAGE_TABLE_NAME=${STORAGE_TABLE_NAME:-Predictions}

echo 'creating app service plan'
echo ". name: $WEB_APP_PLAN_NAME"
#'if' is a workaround for https://github.com/Azure/azure-cli/issues/9833
if [ -z "$(az appservice plan show -g $RESOURCE_GROUP -n $WEB_APP_PLAN_NAME)" ]; then
  az appservice plan create -g $RESOURCE_GROUP -n $WEB_APP_PLAN_NAME \
    --is-linux \
    --number-of-workers $WEB_APP_WORKERS --sku $WEB_APP_SKU \
    -o tsv
fi

echo 'creating web app with initial dummy container'
echo ". name: $WEB_APP_NAME"
echo ". container: $WEB_APP_DUMMY_CONTAINER"
az webapp create -g $RESOURCE_GROUP -n $WEB_APP_NAME \
    --plan $WEB_APP_PLAN_NAME \
    --deployment-container-image-name $WEB_APP_DUMMY_CONTAINER \
    -o none

echo 'setting web app to always on'
az webapp config set -g $RESOURCE_GROUP -n $WEB_APP_NAME --always-on true -o none

echo 'setting web app logging configuration'
az webapp log config -g $RESOURCE_GROUP -n $WEB_APP_NAME \
  --web-server-logging filesystem \
  --docker-container-logging filesystem \
  -o none

echo 'getting connection strings'
TABLE_CS="TableEndpoint=$(az storage account show -n $AZURE_STORAGE_ACCOUNT --query primaryEndpoints.table -o tsv);SharedAccessSignature=$(az storage table generate-sas --account-name $AZURE_STORAGE_ACCOUNT --policy-name table-add -n $STORAGE_TABLE_NAME -o tsv)"

echo 'adding app settings for connection strings'
az functionapp config appsettings set --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
      SQL_DRIVER="{ODBC Driver 17 for SQL Server}" \
      SQL_SERVER="tcp:$SQL_SERVER_NAME.database.windows.net" \
      SQL_DB="$SQL_DATABASE_NAME" \
      SQL_USER="$SQL_ADMIN_USER" \
      SQL_PW="$SQL_ADMIN_PASS" \
      TableStorageConnectionString="$TABLE_CS" \
    -o none
