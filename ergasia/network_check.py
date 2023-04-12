import os

wifi_networks = [
    {
        "ssid": "RPI400",
        "password": "helloErgasia",
        "key_mgmt": "WPA-PSK",
        "priority": 1,
    },
    {
        "ssid": "RPI3B1",
        "password": "helloErgasia",
        "key_mgmt": "WPA-PSK",
        "priority": 2,
    },
]

wpa_supplicant_path = "/etc/wpa_supplicant/wpa_supplicant.conf"

# Read the existing content of the wpa_supplicant.conf file
with open(wpa_supplicant_path, "r") as f:
    file_content = f.readlines()

# Remove existing network blocks
file_content = [line for line in file_content if "network=" not in line]

# Add new network blocks
for network in wifi_networks:
    network_block = f'network={{\n    ssid="{network["ssid"]}"\n    psk="{network["password"]}"\n    key_mgmt={network["key_mgmt"]}\n    priority={network["priority"]}\n}}\n'
    file_content.append(network_block)

# Write the updated content back to the wpa_supplicant.conf file
with open(wpa_supplicant_path, "w") as f:
    f.writelines(file_content)

# Reconfigure the Wi-Fi interface
os.system("sudo wpa_cli -i wlan0 reconfigure")