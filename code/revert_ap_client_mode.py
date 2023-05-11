import subprocess
from pathlib import Path
import os


def revert_to_ap_mode():
    # Enable hostapd service
    subprocess.run(['sudo', 'systemctl', 'unmask', 'hostapd'], check=True)
    subprocess.run(['sudo', 'systemctl', 'enable', 'hostapd'], check=True)

    # Backup the original dhcpcd.conf file and configure the static IP
    if Path('/etc/dhcpcd.conf').exists():
        subprocess.run(['sudo', 'cp', '/etc/dhcpcd.conf', '/etc/dhcpcd.conf.orig'])
        print('dhcpcd.conf has been backed up successfully.')

    if Path('/etc/dhcpcd.conf.setup').exists():
        subprocess.run(['sudo', 'cp', '/etc/dhcpcd.conf.setup', '/etc/dhcpcd.conf'])
        print('dhcpcd.conf has been updated with the new file successfully.')

    # Backup the original hostapd.conf file and configure the access point
    if Path('/etc/hostapd/hostapd.conf').exists():
        subprocess.run(['sudo', 'cp', '/etc/hostapd/hostapd.conf', '/etc/hostapd/hostapd.conf.orig'])
        print('hostapd.conf has been backed up successfully.')

    if Path('/etc/hostapd/hostapd.conf.setup').exists():
        subprocess.run(['sudo', 'cp', '/etc/hostapd/hostapd.conf.setup', '/etc/hostapd/hostapd.conf'])
        print('hostapd.conf has been updated with the new file successfully.')

    # Start hostapd service
    subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'], check=True)

    # Backup the original dnsmasq.conf file and configure the DHCP and DNS settings
    if Path('/etc/dnsmasq.conf').exists():
        subprocess.run(['sudo', 'cp', '/etc/dnsmasq.conf', '/etc/dnsmasq.conf.orig'])
        print('dnsmasq.conf has been backed up successfully.')

    if Path('/etc/dnsmasq.conf.setup').exists():
        subprocess.run(['sudo', 'cp', '/etc/dnsmasq.conf.setup', '/etc/dnsmasq.conf'])
        print('dnsmasq.conf has been updated with the new file successfully.')

    # Enable IPv4 forwarding
    if not Path('/etc/sysctl.d/routed-ap.conf').exists():
        subprocess.run(['sudo', 'sh', '-c', 'echo "# Enable IPv4 routing" > /etc/sysctl.d/routed-ap.conf'])
        subprocess.run(['sudo', 'sh', '-c', 'echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/routed-ap.conf'])

    subprocess.run(['sudo', 'sysctl', '-p', '/etc/sysctl.d/routed-ap.conf'])

    # Configure the firewall
    subprocess.run(['sudo', 'iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'eth0', '-j', 'MASQUERADE'])
    # Save the firewall rules to the netfilter-persistent configuration file
    subprocess.run(['sudo', 'netfilter-persistent', 'save'])

    # Restart the hostapd, dnsmasq and dhcpcd services

    subprocess.run(['sudo', 'systemctl', 'restart', 'dnsmasq'])
    subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'])
    subprocess.run(['sudo', 'systemctl', 'restart', 'hostapd'])
    print("AP setup complete.")
    print('dhcpcd, hostapd and dnsmasq have been restarted!')

    # Prompt the user to confirm the reboot
    # user_input = input("Is the new network active? (y/n)")
    #
    # if user_input.lower() == "y" or user_input.lower() == "yes":
    #     print("You can enjoy, your new network now.")
    # else:
    #     subprocess.run(['sudo', 'systemctl', 'restart', 'hostapd'])


def revert_to_client_mode():
    # Stop and disable hostapd and dnsmasq services
    os.system("sudo systemctl stop hostapd")
    os.system("sudo systemctl disable hostapd")
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo systemctl disable dnsmasq")

    # Restore original dhcpcd.conf file
    os.system("sudo cp /etc/dhcpcd.conf.orig /etc/dhcpcd.conf")
    print("Original dhcpcd.conf has been restored.")

    # Restore original hostapd.conf file
    os.system("sudo cp /etc/hostapd/hostapd.conf.orig /etc/hostapd/hostapd.conf")
    print("Original hostapd.conf has been restored.")

    # Restore original dnsmasq.conf file
    os.system("sudo cp /etc/dnsmasq.conf.orig /etc/dnsmasq.conf")
    print("Original dnsmasq.conf has been restored.")

    # Restart the dhcpcd service
    os.system("sudo systemctl restart dhcpcd")
    print("dhcpcd service has been restarted.")
    # Restore original hostapd.conf file
