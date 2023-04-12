#!/bin/bash

# Step 1: Stop and disable hostapd and dnsmasq services
sudo systemctl stop hostapd
sudo systemctl disable hostapd
sudo systemctl stop dnsmasq
sudo systemctl disable dnsmasq

# Step 2: Restore the original configuration files
if [ -e /etc/dhcpcd.conf.orig ]
then
    sudo mv /etc/dhcpcd.conf.orig /etc/dhcpcd.conf
fi

if [ -e /etc/dnsmasq.conf.orig ]
then
    sudo mv /etc/dnsmasq.conf.orig /etc/dnsmasq.conf
fi

if [ -e /etc/hostapd/hostapd.conf.orig ]
then
    sudo mv /etc/hostapd/hostapd.conf.orig /etc/hostapd/hostapd.conf
fi

# Step 3: Remove the iptables rules
sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -D FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -D FORWARD -i wlan0 -o eth0 -j ACCEPT

# Step 4: Save the iptables rules
sudo sh -c "iptables-save > /etc/iptables/rules.v4"

# Step 5: Revert the IP forwarding changes
sudo sed -i 's/^net.ipv4.ip_forward=1/#net.ipv4.ip_forward=1/' /etc/sysctl.conf
sudo sysctl -p

# Step 6: Restart the dhcpcd service and reboot the Raspberry Pi
sudo systemctl restart dhcpcd

