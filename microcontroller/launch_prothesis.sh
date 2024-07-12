#!/bin/bash

# Name of the conda environment
CONDA_ENV_NAME="5IABD"

# Path to the Python script
PYTHON_SCRIPT_PATH="/home/enzol/5IABD_PA/microcontroller/src/launch.py"

# Activate the conda environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV_NAME"

# Run the Python script
python "$PYTHON_SCRIPT_PATH"

# Deactivate the conda environment (optional)
conda deactivate