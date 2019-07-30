#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT:-${PREFIX}}
EVENTHUB_NAMESPACE=${EVENTHUB_NAMESPACE:-${PREFIX}ehubs}
EVENTHUB_CAPACITY=${EVENTHUB_CAPACITY:-1}
EVENTHUB_NAME_TELEMETRY=${EVENTHUB_NAME_TELEMETRY:-telemetry}
EVENTHUB_NAME_PREDICTION=${EVENTHUB_NAME_PREDICTION:-prediction}
EVENTHUB_PARTITIONS=${EVENTHUB_PARTITIONS:-2}
EVENTHUB_CG=${EVENTHUB_CG:-quality}

echo 'creating eventhubs namespace'
echo ". resource group: $RESOURCE_GROUP"
echo ". name: $EVENTHUB_NAMESPACE"
echo ". capacity: $EVENTHUB_CAPACITY"
echo ". event hubs:"
echo " - $EVENTHUB_NAME_TELEMETRY"
echo " - $EVENTHUB_NAME_PREDICTION"
echo ". partitions: $EVENTHUB_PARTITIONS"
echo ". capture storage account: $AZURE_STORAGE_ACCOUNT"
echo ". consumer group: $EVENTHUB_CG"
echo ". auto-inflate: false"

az eventhubs namespace create -n $EVENTHUB_NAMESPACE -g $RESOURCE_GROUP \
    --sku Standard --capacity $EVENTHUB_CAPACITY \
    --enable-auto-inflate false \
    -o tsv

for eventHub in "$EVENTHUB_NAME_TELEMETRY" "$EVENTHUB_NAME_PREDICTION"
do

  echo 'creating eventhub instance'
  echo ". name: $eventHub"
  echo ". partitions: $EVENTHUB_PARTITIONS"
  
  az eventhubs eventhub create -n $eventHub -g $RESOURCE_GROUP \
      --message-retention 1 --partition-count $EVENTHUB_PARTITIONS --namespace-name $EVENTHUB_NAMESPACE \
      --enable-capture true --capture-interval 300 --capture-size-limit 314572800 \
      --archive-name-format '{Namespace}/{EventHub}/{Year}_{Month}_{Day}_{Hour}_{Minute}_{Second}_{PartitionId}' \
      --blob-container eventhubs \
      --destination-name 'EventHubArchive.AzureBlockBlob' \
      --storage-account $AZURE_STORAGE_ACCOUNT \
      -o tsv
  
  echo 'creating consumer group'
  echo ". name: $EVENTHUB_CG"
  
  az eventhubs eventhub consumer-group create -n $EVENTHUB_CG -g $RESOURCE_GROUP \
      --eventhub-name $eventHub --namespace-name $EVENTHUB_NAMESPACE \
      -o tsv
done
  
