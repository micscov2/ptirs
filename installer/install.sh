#!/bin/bash

# Set environment variables
# This flag will enable debug information for flask
export FLASK_DEBUG=1

# Installing MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# TODO: Check if MongoDB is running

# Installing system dependencies
sudo apt-get update 
sudo apt-get install python-pip

# Install python dependencies
sudo pip install -r requirements.txt 
