#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}
STORAGE_TABLE_NAME=${STORAGE_TABLE_NAME:-Predictions}

echo 'creating storage account'
echo ". name: $AZURE_STORAGE_ACCOUNT"

az storage account create -n $AZURE_STORAGE_ACCOUNT -g $RESOURCE_GROUP --sku Standard_LRS \
    -o tsv

az storage table create --account-name $AZURE_STORAGE_ACCOUNT -n $STORAGE_TABLE_NAME \
    -o tsv
az storage table policy create --account-name $AZURE_STORAGE_ACCOUNT -n table-add -t $STORAGE_TABLE_NAME --permissions a \
    -o tsv

