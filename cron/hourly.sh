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
python "${EXPENDITURE_DIRECTORY}/submit_automated_expenditure.py"
python "${EXPENDITURE_DIRECTORY}/export_expenditure_to_csv.py"
python "${EXPENDITURE_DIRECTORY}/import_and_merge_expenditure.py"
python "${INCOME_DIRECTORY}/submit_automated_income.py"
python "${INCOME_DIRECTORY}/export_income_to_csv.py"
python "${INCOME_DIRECTORY}/import_and_merge_income.py"

deactivate
echo "${today} - END $(basename ${0})"
