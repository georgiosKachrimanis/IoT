#!/bin/bash

# Replace these variables with your desired network name and password
SSID="pi1"
PASSWORD="helloErgasia"

# Update the package list and upgrade the system
sudo apt update
sudo apt upgrade -y

# Install the required packages
sudo apt install hostapd dnsmasq -y

# Enable and start the hostapd service
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

# We keep a backup file of the original configuration first!
if [ -e /etc/dhcpcd.conf ]
then
    sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.orig
fi

# Configure a static IP for the wireless interface
sudo bash -c "cat <<EOF >> /etc/dhcpcd.conf
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOF"

# Restart the dhcpcd service
sudo systemctl restart dhcpcd

# We keep a backup file of the original configuration first!

# Configuring the hostapd, name, password etc.
if [ -e /etc/hostapd/hostapd.conf ]
then
    sudo cp /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.orig
fi
# Configure the access point
sudo bash -c "cat <<EOF > /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=$SSID
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$PASSWORD
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF"
# Copying the original configuration file of dnsmasq
if [ -e /etc/dnsmasq.conf ]
then
  sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
fi

# Configure the DHCP and DNS settings
sudo bash -c "cat <<EOF >> /etc/dnsmasq.conf
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.200,255.255.255.0,24h
EOF"

# Restart the dnsmasq service
sudo systemctl restart dnsmasq

# Enable IP forwarding
sudo sed -i 's/^#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
sudo sysctl -p

# Configure the firewall
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

# Save the firewall rules
sudo sh -c "iptables-save > /etc/iptables/rules.v4"

# Clean up useless files
sudo apt autoremove

# Reboot the Raspberry Pi to apply the changes
sudo reboot
