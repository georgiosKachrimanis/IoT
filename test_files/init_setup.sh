#!/bin/bash

# Update OS
sudo apt update
sudo apt upgrade -y

# Enable SSH
sudo systemctl enable ssh --now
echo "SSH is enabled!"


# Remove unnecessary files
sudo apt autoremove -y
