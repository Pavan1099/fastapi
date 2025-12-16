#!/bin/bash

# setup_and_run.sh
# Automates the setup and launch of the Inventory Management System on a new device.

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure we are running from the script's directory (fastapi/)
# This prevents issues if run from outside like: ./fastapi/setup_and_run.sh
cd "$(dirname "$0")"

echo "🚀 Starting Inventory System Setup..."
echo "📂 Working Directory: $(pwd)"

# 1. Check for Python 3
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# 2. Create Virtual Environment (if it doesn't exist)
VENV_NAME="venv"
if [ ! -d "$VENV_NAME" ]; then
    echo "📦 Creating virtual environment '$VENV_NAME'..."
    $PYTHON_CMD -m venv $VENV_NAME
else
    echo "ℹ️  Virtual environment '$VENV_NAME' already exists."
fi

# Define paths to venv binaries for robustness
PIP_CMD="./$VENV_NAME/bin/pip"
STREAMLIT_CMD="./$VENV_NAME/bin/streamlit"

# 3. Install Dependencies using venv's pip explicitly
if [ -f "requirements.txt" ]; then
    echo "⬇️  Installing/Updating dependencies from requirements.txt..."
    $PIP_CMD install --upgrade pip -q
    $PIP_CMD install -r requirements.txt -q
    echo "✅ Dependencies installed."
else
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

# 4. Run the Application using venv's streamlit explicitly
echo "🎉 Setup complete! Launching Streamlit App..."
echo "---"

$STREAMLIT_CMD run streamlit_app.py
