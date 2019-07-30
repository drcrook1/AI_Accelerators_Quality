#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}

echo 'creating storage account'
echo ". name: $AZURE_STORAGE_ACCOUNT"

az storage account create -n $AZURE_STORAGE_ACCOUNT -g $RESOURCE_GROUP --sku Standard_LRS \
    -o tsv
