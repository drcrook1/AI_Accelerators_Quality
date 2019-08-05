#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}
AML_WORKSPACE=${AML_WORKSPACE:-${PREFIX}azml}
AML_STORAGE=${AML_STORAGE:-${PREFIX}azml}
AML_KEYVAULT=${AML_KEYVAULT:-${PREFIX}azml}
AML_APPINSIGHTS=${AML_APPINSIGHTS:-${PREFIX}azml}
AML_REGISTRY=${AML_REGISTRY:-${PREFIX}azml}

echo 'creating storage account'
echo ". name: $AML_STORAGE"

az storage account create -n $AML_STORAGE -g $RESOURCE_GROUP \
  --kind StorageV2 --sku Standard_LRS \
  -o none

echo 'creating application insights'
echo ". name: $AML_APPINSIGHTS"

az resource create \
    --resource-group $RESOURCE_GROUP \
    --resource-type "Microsoft.Insights/components" \
    --name $AML_APPINSIGHTS \
    --properties '{"Application_Type":"web"}' \
    -o none

echo 'creating key vault'
echo ". name: $AML_KEYVAULT"

az keyvault create -g $RESOURCE_GROUP -n $AML_KEYVAULT -o none

echo "creating container registry"
echo ".name: $AML_REGISTRY"

az acr create -g $RESOURCE_GROUP -n $AML_REGISTRY --sku Basic --admin-enabled true \
  -o none

echo "creating Azure ML workspace"
echo ".name: $AML_WORKSPACE"

az ml workspace create -g $RESOURCE_GROUP -w $AML_WORKSPACE \
 --storage-account $(az storage account show -n $AML_STORAGE --query id -o tsv) \
 --keyvault $(az keyvault show -g $RESOURCE_GROUP -n $AML_KEYVAULT --query id -o tsv) \
 --application-insights $(az resource show -g $RESOURCE_GROUP  --resource-type "Microsoft.Insights/components" -n $AML_APPINSIGHTS --query id -o tsv) \
 --container-registry $(az acr show -g $RESOURCE_GROUP -n $AML_REGISTRY --query id -o tsv) \
 --exist-ok \
 -o none
