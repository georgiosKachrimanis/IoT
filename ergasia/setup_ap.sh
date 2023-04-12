#! /bin/bash

# This is the installation of access point network. The RPi creates and manages a new netwrok.
# The wiFi network is going to be 192.168.4.0/24
# Step 1: Installing the access point software --> hostapd

sudo apt install hostapd -y
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hotapd


#Step 2: Enable the wireless access point service and set it to start when your Raspberry Pi boots
sudo sh -c 'systemctl unmask hostapd && systemctl enable hostapd'

# Step 3: In order to provide network management services (DNS, DHCP) to wireless clients,
# the Raspberry Pi needs to have the dnsmasq software package installed.
sudo apt install dnsmasq -y
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

# We keep a back up file of the original configuration first!
# We keep a backup file of the original configuration first!
if [ -e /etc/dhcpcd.conf ]
then
    sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.orig
fi
# Now Copy the new configuration file Do not forget to change the network for each of the RPIs
sudo cp dhcpcd.conf /etc

# We will allow the users to access the internet (ethernet port used) this is for test reasons
# in order to see if the access point is working.
sudo sh -c 'echo "# Enable IPv$ routing" >> /etc/sysctl.d/routed-ap.conf && echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/routed-ap.conf'

# Adding firewall rules in the Raspberry Pi
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo netfilter-persistent save

# Configure the DHCP and DNS services of the wireless network
# Copying the original configuration file of dnsmasq
if [ -e /etc/dnsmasq.conf ]
then
  sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
fi

sudo cp hostapd.conf /etc/hostapd/hostapd.conf

# Configuring the hostapd, name, password etc.
if [ -e /etc/hostapd/hostapd.conf ]
then
    sudo cp /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.orig
fi

sudo cp hostapd.conf /etc/hostapd/hostapd.conf

# System reboot
sudo systemctl reboot
