#!/bin/bash

# Installing system dependencies
# TODO: Install mongodb
sudo apt-get update >> debug.log
sudo apt-get install python-pip >> debug.log


# Install python dependencies
sudo pip install -r requirements.txt >> debug.log
