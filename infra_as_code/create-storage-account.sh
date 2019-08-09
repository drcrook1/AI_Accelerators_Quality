#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}
STORAGE_TABLE_NAME=${STORAGE_TABLE_NAME:-Predictions}

echo 'creating storage account'
echo ". name: $AZURE_STORAGE_ACCOUNT"

az storage account create -n $AZURE_STORAGE_ACCOUNT -g $RESOURCE_GROUP --sku Standard_LRS \
    -o none

echo 'creating storage container'
echo ". name: telemetry"
az storage container create --account-name $AZURE_STORAGE_ACCOUNT -n telemetry \
    -o none
az storage container policy create --account-name $AZURE_STORAGE_ACCOUNT -n telemetry-read -c telemetry --permissions lr \
    -o none

echo 'creating storage file share'
echo ". name: models"
az storage container create --account-name $AZURE_STORAGE_ACCOUNT -n models \
    -o none

echo 'creating storage table'
echo ". name: $STORAGE_TABLE_NAME"
az storage table create --account-name $AZURE_STORAGE_ACCOUNT -n $STORAGE_TABLE_NAME \
    -o none
az storage table policy create --account-name $AZURE_STORAGE_ACCOUNT -n table-add -t $STORAGE_TABLE_NAME --permissions a \
    -o none

