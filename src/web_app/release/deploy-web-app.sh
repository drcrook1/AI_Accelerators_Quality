#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

RESOURCE_GROUP=${RESOURCE_GROUP-${PREFIX}}
CONTAINER_REGISTRY=${CONTAINER_REGISTRY-${PREFIX}acr}
WEB_APP_NAME=${WEB_APP_NAME:-${PREFIX}"web"}
CONTAINER_TAG=${CONTAINER_TAG:-ai_acc_webapp:latest}

echo "getting ACR credentials"
echo ". Registry: $CONTAINER_REGISTRY"
REGISTRY_LOGIN_SERVER=$(az acr show -n $CONTAINER_REGISTRY --query loginServer -o tsv)
REGISTRY_LOGIN_USER=$(az acr credential show -n $CONTAINER_REGISTRY --query username -o tsv)
REGISTRY_LOGIN_PASS=$(az acr credential show -n $CONTAINER_REGISTRY --query passwords[0].value -o tsv)

echo "Setting webapp container"
echo ". Webapp: $WEB_APP_NAME"
az webapp config container set -g $RESOURCE_GROUP -n $WEB_APP_NAME \
  --docker-custom-image-name "$REGISTRY_LOGIN_SERVER/$CONTAINER_TAG" \
  --docker-registry-server-url  "$REGISTRY_LOGIN_SERVER" \
  --docker-registry-server-user "$REGISTRY_LOGIN_USER" \
  --docker-registry-server-pass "$REGISTRY_LOGIN_PASS" \
  -o table

webapp_url="https://$(az webapp show -g $RESOURCE_GROUP -n $WEB_APP_NAME | jq -r .defaultHostName)"

echo "Warming up webapp"
echo ". URL: $webapp_url"

function smoke_test {
  echo
  echo "Trying to access webapp..."
  curl --silent --show-error --fail --write-out '%{http_code}' --output /dev/null $webapp_url
}
for i in {1..120}; do smoke_test && break || sleep 5; done
echo

echo "Webapp successfully deployed"
echo ". URL: $webapp_url"
