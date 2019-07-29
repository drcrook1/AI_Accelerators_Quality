#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

echo 'creating eventhubs namespace'
echo ". name: $EVENTHUB_NAMESPACE"
echo ". capacity: $EVENTHUB_CAPACITY"
echo ". auto-inflate: false"

az eventhubs namespace create -n $EVENTHUB_NAMESPACE -g $RESOURCE_GROUP \
    --sku Standard --location $LOCATION --capacity $EVENTHUB_CAPACITY \
    --enable-auto-inflate false \
    -o tsv >> log.txt

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
      -o tsv >> log.txt
  
  echo 'creating consumer group'
  echo ". name: $EVENTHUB_CG"
  
  az eventhubs eventhub consumer-group create -n $EVENTHUB_CG -g $RESOURCE_GROUP \
      --eventhub-name $eventHub --namespace-name $EVENTHUB_NAMESPACE \
      -o tsv >> log.txt
done
  
