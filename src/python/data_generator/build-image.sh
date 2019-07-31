#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP:-${PREFIX}}
CONTAINER_REGISTRY=${CONTAINER_REGISTRY:-${PREFIX}acr}
PYTHON_PACKAGE_REPO=${PYTHON_PACKAGE_REPO}
IMAGE_TAG=${BUILD_BUILDID:-latest}

echo "building generator container..."

az acr build --registry $CONTAINER_REGISTRY --image generator:$IMAGE_TAG \
  --secret-build-arg IMAGE_SERVER=$PYTHON_PACKAGE_REPO \
  . \
  -o tsv
