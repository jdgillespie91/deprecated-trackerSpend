#!/bin/bash

today=$(date +"%Y-%m-%d %H:%M:%S")

echo "${today} - START $(basename ${0})"
source "/home/ec2-user/trackerSpend/env/bin/activate"

# Global variables.
export BASE_DIRECTORY="/home/ec2-user/trackerSpend"

export CRON_DIRECTORY="${BASE_DIRECTORY}/cron"
export DATA_DIRECTORY="${BASE_DIRECTORY}/data"
export ENV_DIRECTORY="${BASE_DIRECTORY}/env"
export ETL_DIRECTORY="${BASE_DIRECTORY}/etl"

export EXPENDITURE_DIRECTORY="${DATA_DIRECTORY}/expenditure"
export INCOME_DIRECTORY="${DATA_DIRECTORY}/income"

export EXPENDITURE_EXPORTS_DIRECTORY="${EXPENDITURE_DIRECTORY}/exports"

export INCOME_EXPORTS_DIRECTORY="${INCOME_DIRECTORY}/exports"

# Scripts.
python "${EXPENDITURE_DIRECTORY}/submit_automated_expenditure.py"
python "${INCOME_DIRECTORY}/submit_automated_income.py"
python "${BASE_DIRECTORY}/utils/remove_icon_files.py"

deactivate
echo "${today} - END $(basename ${0})"
