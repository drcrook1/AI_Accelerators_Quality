#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
CONTAINER_REGISTRY=${CONTAINER_REGISTRY-${PREFIX}acr}
EVENTHUB_NAMESPACE=${EVENTHUB_NAMESPACE:-${PREFIX}ehubs}
EVENTHUB_NAME_TELEMETRY=${EVENTHUB_NAME_TELEMETRY:-telemetry}
TEST_CLIENTS=${TEST_CLIENTS:-1}

echo 'getting event hub key'
eventHubKey=`az eventhubs namespace authorization-rule keys list --name RootManageSharedAccessKey --namespace-name $EVENTHUB_NAMESPACE --resource-group $RESOURCE_GROUP --query 'primaryKey' -o tsv`

echo 'getting ACR credentials'
REGISTRY_LOGIN_SERVER=$(az acr show -n $CONTAINER_REGISTRY --query loginServer -o tsv)
REGISTRY_LOGIN_PASS=$(az acr credential show -n $CONTAINER_REGISTRY --query passwords[0].value -o tsv)

echo 'create test clients'
echo ". count: $TEST_CLIENTS"

echo "deploying locust..."
locust_output=$(az group deployment create -g $RESOURCE_GROUP --template-file locust.arm.json --parameters eventHubNamespace=$EVENTHUB_NAMESPACE eventHubName=$EVENTHUB_NAME_TELEMETRY eventHubKey=$eventHubKey fileShareName=locust numberOfInstances=$TEST_CLIENTS imageRegistry=$REGISTRY_LOGIN_SERVER imageRegistryUsername=$CONTAINER_REGISTRY imageRegistryPassword=$REGISTRY_LOGIN_PASS)
locustMonitor=$(jq -r .properties.outputs.locustMonitor.value <<< "$locust_output")
sleep 10

echo ". endpoint: $locustMonitor"

echo "starting locust swarm..."
declare userCount=$((250*$TEST_CLIENTS))
declare hatchRate=$((10*$TEST_CLIENTS))
echo ". users: $userCount"
echo ". hatch rate: $hatchRate"
curl $locustMonitor/swarm -X POST -F "locust_count=$userCount" -F "hatch_rate=$hatchRate"

echo 'done'
echo 'starting to monitor locusts for 20 seconds... '
sleep 5
for s in {1..10}; do
    rps=$(curl -s -X GET $locustMonitor/stats/requests | jq ".stats[0].current_rps")
    echo "locust is sending $rps messages/sec"
    sleep 2
done
echo 'monitoring done'

echo "locust monitor available at: $locustMonitor"
