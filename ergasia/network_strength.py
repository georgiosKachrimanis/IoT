import subprocess
import re

# Run the 'iw' command and get the output
cmd_output = subprocess.check_output(['sudo', 'iw', 'dev', 'wlan0', 'scan']).decode('utf-8')

# Regex patterns to match SSIDs and signal strengths
ssid_pattern = re.compile(r"SSID: (.+)")
signal_strength_pattern = re.compile(r"signal: ([-\d]+)")

# Extract SSIDs and signal strengths
ssids = ssid_pattern.findall(cmd_output)
signal_strengths = [int(x) for x in signal_strength_pattern.findall(cmd_output)]

# Combine SSIDs and signal strengths into a list of tuples
networks = list(zip(ssids, signal_strengths))

# Sort the list in descending order by signal strength
sorted_networks = sorted(networks, key=lambda x: x[1], reverse=True)

# Print the sorted list
for ssid, strength in sorted_networks:
    print(f"SSID: {ssid}, Signal strength: {strength} dBm")
