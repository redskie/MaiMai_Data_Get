#!/bin/bash

echo "Installing dependencies..."

# Install Python dependencies first
pip install -r requirements.txt

echo "Build complete!"
echo "Note: Render should have Chrome pre-installed or use webdriver-manager"
