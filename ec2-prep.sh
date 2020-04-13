#!/bin/bash
# Install Python3
sudo yum -y install python36
# Install PIP3
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
# Install required Python packages in user-specific directories
pip3 install luigi --user
pip3 install boto3 --user
pip3 install psycopg2 --user
pip3 install requests --user
pip3 install re --user
pip3 install bs4 --user
pip3 install time --user
pip3 install csv --user
pip3 install datetime --user