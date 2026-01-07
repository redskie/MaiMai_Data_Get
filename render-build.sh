#!/bin/bash

# Install Chrome dependencies
apt-get update
apt-get install -y wget gnupg

# Add Google Chrome repository
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
apt-get update
apt-get install -y google-chrome-stable

# Verify installation
google-chrome --version

# Install Python dependencies
pip install -r requirements.txt
