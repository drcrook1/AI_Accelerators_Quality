#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
CONTAINER_REGISTRY=${CONTAINER_REGISTRY-${PREFIX}acr}

echo "creating container registry..."
az acr create -g $RESOURCE_GROUP -n $CONTAINER_REGISTRY --sku Basic --admin-enabled true \
  -o tsv
