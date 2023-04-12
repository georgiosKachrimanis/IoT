#!/bin/bash

# Change to the /etc/network directory
cd /etc/network

# Restore the original wifi interface file
sudo cp wifi-interface interfaces

# Restart the networking service
sudo service networking restart
