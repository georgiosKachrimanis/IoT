import os
import sys
# Get the username of the current user
username = os.getlogin()


def create_hostapd(user):
    # Read the contents of the original hostapd.conf file
    with open("/etc/hostapd/hostapd.conf", "r") as file:
        original_contents = file.read()

    # Append the additional configuration to the original contents
    config = f"""
interface=wlan0
driver=nl80211
ssid={user}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=helloErgasia
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""

    new_contents = original_contents + config

    # Write the new contents to the hostapd.conf.setup file
    with open("hostapd.conf.setup", "w") as file:
        file.write(new_contents)


def create_dnsmasq(user):

    # Check if the dnsmasq.conf file exists and install it if not.(If you forgot to run first_setup.py)
    if not os.path.exists("/etc/dnsmasq.conf"):
        installation_successful = install_dnsmasq()
        if not installation_successful:
            print("Error: Failed to install dnsmasq.")
            return

    # Extract the numerical part of the username
    user_number = get_user_number(user)

    # Set the DHCP range based on the username number
    dhcp_range = f"192.168.{user_number}.2,192.168.{user_number}.200,255.255.255.0,24h"

    # Set the static IP address for the specific laptop
    static_ip = f"192.168.{user_number}.200"

    # Replace the MAC_ADDRESS with the actual MAC address of your laptop
    mac_address = "50:ed:3c:34:6e:f7"

    # Read the contents of the original dnsmasq.conf file
    with open("/etc/dnsmasq.conf", "r") as file:
        original_contents = file.read()

    # Append the additional configuration to the original contents
    config = f"""
interface=wlan0
dhcp-range={dhcp_range}
dhcp-host={mac_address},{static_ip}
        """

    new_contents = original_contents + config

    # Write the new contents to the dnsmasq.conf.setup file
    with open("dnsmasq.conf.setup", "w") as file:
        file.write(new_contents)


def create_dhcpcd(user):
    user_number = get_user_number(user)

    # Set the static IP address based on the user number
    static_ip = f"192.168.{user_number}.1/24"

    # Read the contents of the original dhcpcd.conf file
    with open("/etc/dhcpcd.conf", "r") as file:
        original_contents = file.read()

    # Append the additional configuration to the original contents
    config = f"""
interface wlan0
    static ip_address={static_ip}
    nohook wpa_supplicant
    """

    new_contents = original_contents + config

    # Write the new contents to the dhcpcd.conf.setup file
    with open("dhcpcd.conf.setup", "w") as file:
        file.write(new_contents)


def get_user_number(user):
    # Extract the numerical part of the username
    user_number = int("".join(filter(str.isdigit, user)))

    return user_number


def install_dnsmasq():
    print("Warning: /etc/dnsmasq.conf not found. Installing dnsmasq.")
    result = os.system("sudo apt-get update && sudo apt-get install dnsmasq -y")
    if result == 0:
        return True
    else:
        return False


# Call the functions to create the configuration files
create_dnsmasq(username)
create_hostapd(username)
create_dhcpcd(username)

print("All configuration files have been successfully created.")