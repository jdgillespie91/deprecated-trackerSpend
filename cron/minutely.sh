#!/bin/bash

today=$(date +"%Y-%m-%d %H:%M:%S")

echo "${today} - START $(basename ${0})"
source "/home/ubuntu/.envs/trackerSpend/bin/activate"

# Global variables.

export BASE_DIRECTORY="/home/ubuntu/projects/trackerSpend"
export PYTHONPATH="${PYTHONPATH}:${BASE_DIRECTORY}"

export CRON_DIRECTORY="${BASE_DIRECTORY}/cron"
export DATA_DIRECTORY="${BASE_DIRECTORY}/data"

export EXPENDITURE_DIRECTORY="${DATA_DIRECTORY}/expenditure"
export INCOME_DIRECTORY="${DATA_DIRECTORY}/income"

export EXPENDITURE_EXPORTS_DIRECTORY="${EXPENDITURE_DIRECTORY}/exports"

export INCOME_EXPORTS_DIRECTORY="${INCOME_DIRECTORY}/exports"

# Scripts.

deactivate
echo "${today} - END $(basename ${0})"
