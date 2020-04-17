#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Failed: This script must be run as root" 
   exit 1
fi

# Make sure python and pip are installed
command -v python3 >/dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "Failed: Python 3 is not installed!"
    exit 2
fi

python3 -m pip --version >/dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "Failed: PIP python module is not installed!"
    exit 3
fi

# Install requirements
python3 -m pip install -r requirements.txt
if [[ $? -ne 0 ]]; then
    echo "Failed: Failed to install required modules!"
    exit 4
fi

# Install systemd service
cat << EOF > /etc/systemd/system/tcollector.service
[Unit]
Description=Tibi Collector Service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
ExecStart=/usr/bin/env python3 $(pwd)/collector.py

[Install]
WantedBy=multi-user.target
EOF

systemctl enable tcollector
systemctl stop tcollector
systemctl start tcollector
systemctl status tcollector