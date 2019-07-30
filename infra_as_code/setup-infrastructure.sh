#!/bin/bash

set -euo pipefail

bash create-storage-account.sh
bash create-event-hub.sh
bash create-scoring-function.sh
