import subprocess
from pathlib import Path
import os

SERVICES = ['dhcpcd', 'dnsmasq', 'hostapd']
HOSTAPD = '/etc/hostapd/hostapd.'
DHCPCD = '/etc/dhcpcd.'
DNSMASQ = '/etc/dnsmasq.'


def update_service_file(service):
    """
       Updates the specified service configuration file with the new setup.

       This function first backs up the original {service}.conf file by creating a copy
       named {service}.conf.orig. Then, it replaces the existing {service}.conf file with
       the {service}.conf.setup file, which contains the new configuration.

       Args:
           service (str): The name of the service configuration file to update.

       Raises:
           None.
       """
    if Path(f'{service}.conf').exists():
        subprocess.run(['sudo', 'cp', f'{service}.conf', f'{service}.conf.orig'])
        print(f'{service}.conf has been backed up successfully.')
    else:
        print(f'Error: {service}.conf file not found.')

    if Path(f'{service}.conf.setup').exists():
        subprocess.run(['sudo', 'cp', f'{service}.conf.setup', f'{service}.conf'])
        print(f'{service}.conf has been updated with the new file successfully.')
    else:
        print(f'Error: {service}.conf.setup file not found.')


def enable_ipv4_forwarding():
    """
    Enables IPv4 forwarding by creating or updating the /etc/sysctl.d/routed-ap.conf file.

    This function checks if the /etc/sysctl.d/routed-ap.conf file exists. If not, it creates
    the file and adds the necessary configuration to enable IPv4 routing. If the file already
    exists, it updates the existing configuration. Finally, it reloads the sysctl settings.

    Raises:
        subprocess.CalledProcessError: If there is an error reloading the sysctl settings.
    """
    if not Path('/etc/sysctl.d/routed-ap.conf').exists():
        subprocess.run(['sudo', 'sh', '-c', 'echo "# Enable IPv4 routing" > /etc/sysctl.d/routed-ap.conf'])
        subprocess.run(['sudo', 'sh', '-c', 'echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/routed-ap.conf'])

    subprocess.run(['sudo', 'sysctl', '-p', '/etc/sysctl.d/routed-ap.conf'])


def firewall_config():
    """
    Configures the firewall by setting up NAT (Network Address Translation) and saving the firewall rules.

    This function uses the `iptables` command to configure NAT for outgoing traffic on the `eth0` interface.
    It adds a POSTROUTING rule to perform MASQUERADE, which allows devices in the local network to access
    the internet through the Raspberry Pi. After configuring the firewall, it saves the firewall rules
    to the netfilter-persistent configuration file.

    Raises:
        subprocess.CalledProcessError: If there is an error executing the `iptables` or `netfilter-persistent` commands.
    """
    subprocess.run(['sudo', 'iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'eth0', '-j', 'MASQUERADE'])
    subprocess.run(['sudo', 'netfilter-persistent', 'save'])


def stop_services():
    """
    Stops and disables the hostapd and dnsmasq services.

    Returns:
    None
    """
    os.system("sudo systemctl stop hostapd")
    os.system("sudo systemctl disable hostapd")
    os.system("sudo systemctl stop dnsmasq")
    os.system("sudo systemctl disable dnsmasq")


def restore_service_file(service):
    """
    Restores the original dhcpcd.conf file.

    Returns:
    None
    """
    os.system(f"sudo cp {service}.conf.orig {service}.conf")
    print(f"Original {service}.conf has been restored.")


def restart_service(service):
    """
    Restarts the specified service.

    Args:
        service (str): The name of the service to restart.

    Returns:
        None
    """
    subprocess.run(['sudo', 'systemctl', 'restart', service])
    print(f"{service} service has been restarted.")


def enable_hostapd_service():
    """
    Enables the hostapd service.

    Returns:
    None
    """
    subprocess.run(['sudo', 'systemctl', 'unmask', 'hostapd'], check=True)
    subprocess.run(['sudo', 'systemctl', 'enable', 'hostapd'], check=True)


def update_network_configuration():
    """
    Updates the network configuration files.

    This function updates the dhcpcd.conf, hostapd.conf, and dnsmasq.conf files.

    Returns:
    None
    """

    update_service_file(DHCPCD)
    update_service_file(HOSTAPD)
    # Start hostapd service
    subprocess.run(['sudo', 'systemctl', 'start', 'hostapd'], check=True)
    update_service_file(DNSMASQ)


def revert_to_ap_mode():
    """
    Reverts the device to Access Point (AP) mode.

    This function enables the hostapd service, updates the network configuration files,
    enables IPv4 forwarding, updates the firewall rules, and restarts the network services.

    Returns:
    None
    """
    enable_hostapd_service()
    update_network_configuration()
    enable_ipv4_forwarding()
    firewall_config()
    # Restart the specified services
    for service in SERVICES:
        restart_service(service)

    print("AP setup complete.")
    print('dhcpcd, hostapd, and dnsmasq have been restarted!')


def revert_to_client_mode():
    """
    Reverts the device to client mode.

    This function stops and disables the hostapd and dnsmasq services,
    restores the original dhcpcd.conf, hostapd.conf, and dnsmasq.conf files,
    and restarts the dhcpcd service.

    Returns:
    None
    """
    stop_services()
    restore_service_file(DHCPCD)
    restore_service_file(HOSTAPD)
    restore_service_file(DNSMASQ)
    restart_service("dhcpcd")
