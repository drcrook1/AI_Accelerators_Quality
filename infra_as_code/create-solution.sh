#!/bin/bash

# Strict mode, fail on any error
set -euo pipefail

STEPS="CIPTM"

usage() {
    echo "Usage: $0 -d <deployment-name> [-s <steps>] [-t <test-type>] [-l <location>]" 1>&2;
    echo "-s: specify which steps should be executed. Default=$STEPS" 1>&2;
    echo "    Possible values:" 1>&2;
    echo "      C=COMMON" 1>&2;
    echo "      I=INGESTION" 1>&2;
    echo "      P=PROCESSING" 1>&2;
    echo "      T=TEST clients" 1>&2;
    echo "      M=METRICS reporting" 1>&2;
    echo "-t: test 1,5,10 thousands msgs/sec. Default=1"
    echo "-l: where to create the resources. Default=eastus"
    exit 1;
}

export PREFIX=''
export LOCATION='eastus'
export TESTTYPE='1'

# Initialize parameters specified from command line
while getopts ":d:s:t:l:" arg; do
	case "${arg}" in
		d)
			PREFIX=${OPTARG}
			;;
		s)
			STEPS=${OPTARG}
			;;
		t)
			TESTTYPE=${OPTARG}
			;;
		l)
			LOCATION=${OPTARG}
			;;
		esac
done
shift $((OPTIND-1))

if [[ -z "$PREFIX" ]]; then
	echo "Enter a name for this deployment."
	usage
fi

export PROC_FUNCTION_DIR=../src/python/inference_function
export PROC_FUNCTION_SKU=P2v2

# 10000 messages/sec
if [ "$TESTTYPE" == "10" ]; then
    export EVENTHUB_PARTITIONS=12
    export EVENTHUB_CAPACITY=12
    export PROC_FUNCTION_WORKERS=12
    export TEST_CLIENTS=30
fi

# 5500 messages/sec
if [ "$TESTTYPE" == "5" ]; then
    export EVENTHUB_PARTITIONS=8
    export EVENTHUB_CAPACITY=6
    export PROC_FUNCTION_WORKERS=8
    export TEST_CLIENTS=16
fi

# 1000 messages/sec
if [ "$TESTTYPE" == "1" ]; then
    export EVENTHUB_PARTITIONS=2
    export EVENTHUB_CAPACITY=2
    export TEST_CLIENTS=3
    export PROC_FUNCTION_WORKERS=2
fi

# last checks and variables setup
if [ -z ${TEST_CLIENTS+x} ]; then
    usage
fi

export RESOURCE_GROUP=$PREFIX

# remove log.txt if exists
rm -f log.txt

echo "Checking pre-requisites..."

HAS_AZ=$(command -v az || true)
if [ -z "$HAS_AZ" ]; then
    echo "AZ CLI not found"
    echo "please install it as described here:"
    echo "https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest"
    exit 1
fi

HAS_JQ=$(command -v jq || true)
if [ -z "$HAS_JQ" ]; then
    echo "jq not found"
    echo "please install it using your package manager, for example, on Ubuntu:"
    echo "  sudo apt install jq"
    echo "or as described here:"
    echo "  https://stedolan.github.io/jq/download/"
    exit 1
fi

HAS_ZIP=$(command -v zip || true)
if [ -z "$HAS_ZIP" ]; then
    echo "zip not found"
    echo "please install it using your package manager, for example, on Ubuntu:"
    echo "  sudo apt install zip"
    exit 1
fi

HAS_FUNC=$(command -v func || true)
if [ -z "$HAS_FUNC" ]; then
    echo "Azure Functions Core Tools not found"
    echo "please install them as described here:"
    echo "https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local"
    exit 1
fi

AZ_SUBSCRIPTION_NAME=$(az account show --query name -o tsv || true)
if [ -z "$AZ_SUBSCRIPTION_NAME" ]; then
    #az account show already shows error message "Please run 'az login' to setup account."
    exit 1
fi

echo
echo "AI/ML Accelerator sample for quality detection"
echo "=============================================="
echo

echo "Steps to be executed: $STEPS"
echo

echo "Configuration: "
echo ". Subscription    => $AZ_SUBSCRIPTION_NAME"
echo ". Resource Group  => $RESOURCE_GROUP"
echo ". Region          => $LOCATION"
echo ". EventHubs       => TU: $EVENTHUB_CAPACITY, Partitions: $EVENTHUB_PARTITIONS"
echo ". Function        => SKU: $PROC_FUNCTION_SKU, Workers: $PROC_FUNCTION_WORKERS"
echo ". Locusts         => $TEST_CLIENTS"
echo

echo "Deployment started..."
echo

echo "***** [C] Setting up COMMON resources"

    export AZURE_STORAGE_ACCOUNT=$PREFIX"storage"

    RUN=`echo $STEPS | grep C -o || true`
    if [ ! -z "$RUN" ]; then
        ./01-create-resource-group.sh
        ./02-create-storage-account.sh
    fi
echo

echo "***** [I] Setting up INGESTION"

    export EVENTHUB_NAMESPACE=$PREFIX"eventhubs"
    export EVENTHUB_NAME_TELEMETRY="telemetry-hub"
    export EVENTHUB_NAME_PREDICTION="predictions-hub"
    export EVENTHUB_CG="scoring"

    RUN=`echo $STEPS | grep I -o || true`
    if [ ! -z "$RUN" ]; then
        ./03-create-event-hub.sh
    fi
echo

echo "***** [P] Setting up PROCESSING"

    export PROC_FUNCTION_APP_NAME=$PREFIX"process"

    RUN=`echo $STEPS | grep P -o || true`
    if [ ! -z "$RUN" ]; then
        ./04-create-scoring-function.sh
    fi
echo
echo "***** [T] Starting up TEST clients"

    RUN=`echo $STEPS | grep T -o || true`
    if [ ! -z "$RUN" ]; then
        ./05-run-clients.sh
    fi
echo

echo "***** [M] Starting METRICS reporting"

    RUN=`echo $STEPS | grep M -o || true`
    if [ ! -z "$RUN" ]; then
        ./06-report-throughput.sh
    fi
echo

echo "***** Done"
