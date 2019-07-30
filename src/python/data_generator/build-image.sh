#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
CONTAINER_REGISTRY=${CONTAINER_REGISTRY-${PREFIX}acr}
PYTHON_PACKAGE_REPO=${PYTHON_PACKAGE_REPO}

echo "checking container registry exists..."
if ! az acr show -g $RESOURCE_GROUP -n $CONTAINER_REGISTRY ; then
  echo "creating container registry..."
  az acr create -g $RESOURCE_GROUP -n $CONTAINER_REGISTRY --sku Basic --admin-enabled true \
    -o tsv
fi

echo "building generator container..."

az acr build --registry $CONTAINER_REGISTRY --image generator:latest \
  --secret-build-arg IMAGE_SERVER=$PYTHON_PACKAGE_REPO \
  . \
  -o tsv
