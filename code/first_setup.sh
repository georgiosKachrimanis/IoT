#!/bin/bash

# Update the package list and upgrade the system
sudo apt update
sudo apt upgrade -y

# Install the required packages
sudo apt install dnsmasq -y

# Remove unnecessary files.
sudo apt autoremove -y

