import os

# Get the username of the current user
username = os.getlogin()


def get_pi_number(user):
    """
    Generates the user number based on the current AP.
    Args:
    user (str): The name of the current Access Point.

    Returns:
    user numerical value.
    """
    # Extract the numerical part of the username
    user_number = int("".join(filter(str.isdigit, user)))

    return user_number


def create_hostapd(user):
    """
    Install and  Generates a hostapd configuration file based on the current AP.

    Args:
    user (str): The name of the current Access Point.

    Returns:
    None.
    """
    os.system("sudo apt install hostapd -y")
    os.system("sudo systemctl unmask hostapd")
    os.system("sudo systemctl enable hostapd")
    os.system("sudo touch /etc/hostapd/hostapd.conf")

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
    with open("/etc/hostapd/hostapd.conf.setup", "w") as file:
        file.write(new_contents)

    print("hostapd.conf.setup file was created successfully for {}!".format(user))


def create_dnsmasq(user):
    """
    Install and  Generates a dnsmasq configuration file based on the current AP.

    Args:
    user (str): The name of the current Access Point.

    Returns:
    None.
    """

    # Extract the numerical part of the username
    pi_number = get_pi_number(user)

    # Set the DHCP range based on the username number the range is from 2-250 you can adjust to desired
    dhcp_range = f"192.168.{pi_number}.2,192.168.{pi_number}.200,255.255.255.0,24h"

    os.system("sudo apt install dnsmasq -y")
    print("Installation of dnsmasq was successful")

    # Set the static IP address for the specific laptop
    static_ip = f"192.168.{pi_number}.200"

    # Replace the MAC_ADDRESS with the actual MAC address of your laptop
    mac_address = "50:ed:3c:34:6e:f7"

    # Read the contents of the original dnsmasq.conf file
    with open("/etc/dnsmasq.conf", "r") as file:
        original_contents = file.read()

    # Append the additional configuration to the original contents
    config = f"""
interface=wlan0
dhcp-range={dhcp_range}
domain=wlan
address=/gw.wlan/192.168.{pi_number}.1
dhcp-host={mac_address},{static_ip}
        """

    new_contents = original_contents + config

    # Write the new contents to the dnsmasq.conf.setup file
    with open("/etc/dnsmasq.conf.setup", "w") as file:
        file.write(new_contents)

    print("dnsmasq.conf.setup file was created successfully for pi{}!".format(pi_number))


def create_dhcpcd(user):
    """
    Generates a dhcpcd configuration file based on the current AP.

    Args:
    user (str): The name of the current Access Point.

    Returns:
    None.
    """
    pi_number = get_pi_number(user)

    # Set the static IP address based on the user number
    static_ip = f"192.168.{pi_number}.1/24"

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
    with open("/etc/dhcpcd.conf.setup", "w") as file:
        file.write(new_contents)

    print("dhcpcd.conf.setup file was created successfully for pi{}!".format(pi_number))


def install_apps():
    """
    Installs extra software for  applications to the RPi

    Args:
    none

    Returns:
    boolean for control reasons.
    """

    # Install hostapd and dnsmasq
    print("Upgrading and updating your system")
    result1 = os.system('sudo apt-get install python3-flask -y')
    result2 = os.system("sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent")
    # installing external libraries
    os.system('sudo pip3 install svgwrite -y')

    # Check the result of the installation
    if (result1 == 0) & (result2 == 0):
        return True
    else:
        return False


def adjust_wpa_range(user):
    """
    Creates a wpa_range configuration file with the predetermined
    available wi-fi networks that our nodes are able to connect.

    Args:
    user (str): The name of the current Access Point.

    Returns:
    none
    """
    # Define the parameters all of those parameters should be adjusted depending on your swarm size and location
    country_code = "NL" # You should change to the appropriate country you are using the swarm
    password = "helloErgasia" # This will be the password for the Wi-Fi
    ssid_range = range(2, 199) # The amount of AP you are going to have
    pi_number = get_pi_number(user)

    # Create the base content of the wpa_supplicant.conf file
    content = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country={country_code}\n"""

    # Generate the network configurations for the specified range
    for i in ssid_range:
        if i != pi_number:
            network_config = f"""
        network={{
            ssid="pi{i}"
            psk="{password}"
            key_mgmt=WPA-PSK
        }}"""
            content += network_config

    # Write the content to the wpa_supplicant.conf file
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as file:
        file.write(content)

    print("The list with available networks has been updated!")


def adjust_rc_file():
    """
    Adds a command to the /etc/rc.local file and sets it to executable. The function
    will check if the command is already present before adding it. The command is added
    to fix issues whit IP addressing after restart of the RPi as AP.

    Args:
    None

    Returns:
    None
    """
    # Add command to rc.local
    command = "sudo systemctl restart dhcpcd dnsmasq hostapd"
    rc_local_file = "/etc/rc.local"
    with open(rc_local_file, "r+") as f:
        contents = f.read()
        if command not in contents:
            f.seek(0, 0)
            f.write("#!/bin/sh -e\n")
            f.write(command + "\n")
            f.write("exit 0\n")

    # Make rc.local executable
    os.chmod(rc_local_file, 0o755)


# Call the functions to create the configuration files
if install_apps():

    print("Installation was successful, creating configuration files now!")
    create_dnsmasq(username)
    create_hostapd(username)
    create_dhcpcd(username)
    adjust_wpa_range(username)
    adjust_rc_file()

    print("All configuration files have been successfully created.\n")


# Prompt the user to confirm the reboot
user_input = input("Update complete. Reboot now? (y/n)")

if user_input.lower() == "y" or user_input.lower() == "yes":
    # Run the reboot command
    os.system("sudo reboot")
else:
    print("Reboot cancelled.")
