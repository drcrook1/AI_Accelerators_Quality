#!/bin/bash

set -euo pipefail

bash create-container-registry.sh
bash create-storage-account.sh
bash create-event-hub.sh
bash create-sql-database.sh
bash create-web-app.sh
bash create-scoring-function.sh
