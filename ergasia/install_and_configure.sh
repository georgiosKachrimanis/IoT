#!/bin/bash

# Check if the necessary software is already installed
if ! (dpkg-query -W -f='${Status}' hostapd 2>/dev/null | grep -c "ok installed") || ! (dpkg-query -W -f='${Status}' dnsmasq 2>/dev/null | grep -c "ok installed")
then
  # Update the package list and upgrade the system
  sudo apt update
  sudo apt upgrade -y

  # Install the required packages
  sudo apt install hostapd dnsmasq -y
fi

# Check the mode argument passed to the script
mode=$1

if [ "$mode" == "ap" ]
then
  # Switch to AP mode
  sudo ./ap_mode.sh
elif [ "$mode" == "client" ]
then
  # Switch to client mode
  sudo ./client_mode.sh
else
  echo "Invalid argument. Usage: ./install_and_configure.sh [ap|client]"
fi
