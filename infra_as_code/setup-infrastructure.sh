#!/bin/bash

set -euo pipefail

./create-storage-account.sh
./create-event-hub.sh
./create-scoring-function.sh
