#!/bin/bash

set -euo pipefail

bash create-storage-account.sh
bash create-event-hub.sh
bash create-sql-database.sh
bash create-scoring-function.sh
bash create-container-registry.sh
