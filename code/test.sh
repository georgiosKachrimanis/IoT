#!/bin/bash

# Enable and start the hostapd service
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

# We keep a backup file of the original dhcpcd.conf configuration first!
if [ -e /etc/dhcpcd.conf ]
then
    sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.orig
    echo "dhcpcd.conf has been Backed Up successfully."
fi

# Use the setup file to configure a static IP for the wireless interface
if [ -e /etc/dhcpcd.conf ]
then
    sudo cp /etc/dhcpcd.conf.setup /etc/dhcpcd.conf
    echo "dhcpcd.conf has been updated with the new file successfully."
fi

# Restart the dhcpcd service
sudo systemctl restart dhcpcd

# We keep a backup file of the original hostapd.conf configuration first!
# Configuring the hostapd, name, password etc.
if [ -e /etc/hostapd/hostapd.conf ]
then
    sudo cp /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.orig
    echo "hostapd.conf has been Backed Up successfully."
fi
# Configure the access point
if [ -e /etc/hostapd/hostapd.conf.setup ]
then
    sudo cp /etc/hostapd/hostapd.conf.setup /etc/hostapd/hostapd.conf
    echo "hostapd.conf has been updated with the new file successfully."
fi

# Copying the original configuration file of dnsmasq
if [ -e /etc/dnsmasq.conf ]
then
  sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
  echo "dnsmasq.conf has been Backed Up successfully."
fi

# Configure the DHCP and DNS settings
if [ -e /etc/dnsmasq.conf.setup ]
then
  sudo cp /etc/dnsmasq.conf.setup /etc/dnsmasq.conf
  echo "dnsmasq.conf has been updated with the new file successfully."
fi

# Restart the hostapd service and dnsmasq service
sudo systemctl restart hostapd
sudo systemctl restart dnsmasq

echo "hostapd and dnsmasq have been restarted!"

# Enable IP forwarding
sudo sed -i 's/^#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
sudo sysctl -p

# Configure the firewall
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

# Create and save the firewall rules
sudo mkdir -p /etc/iptables
sudo sh -c "iptables-save > /etc/iptables/rules.v4"

    os.system("sudo apt install hostapd -y")
    os.system("sudo systemctl unmask hostapd")
    os.system("sudo systemctl enable hostapd")