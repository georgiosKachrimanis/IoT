#!/bin/bash

# Change to the /etc/network directory
cd /etc/network

# Make a backup copy of the original wifi interface file
sudo cp interfaces wifi-interface

# Create a new file for the Ad hoc interface and open it for editing
sudo touch ad-hoc-interface

# Add the required text to the ad-hoc-interface file
cat <<EOF | sudo tee ad-hoc-interface > /dev/null
auto lo
iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
iface wlan0 inet static
address 192.168.4.1
netmask 255.255.255.0
wireless-channel 4
wireless-essid RPitest
wireless-mode ad-hoc
EOF

# Install the DHCP server
sudo apt-get install isc-dhcp-server -y

# Make a backup copy of the dhcpcd.conf file
sudo cp /etc/dhcp/dhcpcd.conf /etc/dhcp/dhcpcd.conf.bak

# Add the required parameters to the dhcpcd.conf file
sudo bash -c 'echo "ddns-update-style interim;
  default-lease-time 600;
  max-lease-time 7200;
  authoritative;
  log-facility local7;
  subnet 192.168.4.0 netmask 255.255.255.0 {
  range 192.168.4.5 192.168.4.100;
  }" >> /etc/dhcp/dhcpcd.conf'

# Start the DHCP server
sudo service isc-dhcp-server start

# Restart the networking service
sudo service networking restart