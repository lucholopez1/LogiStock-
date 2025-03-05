#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Update pip (optional)
pip install --upgrade pip

# Install
pip install -r requirements.txt

echo "Entorno virtual configurado con éxito."