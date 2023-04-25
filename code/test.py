import subprocess
import socket
import requests


def list_connected_devices(interface="wlan0"):
    try:
        output = subprocess.check_output(["sudo", "arp-scan", "-l", "-I", interface])
        output_lines = output.decode().split("\n")

        devices = []
        for line in output_lines:
            line_parts = line.split("\t")
            if len(line_parts) == 3:
                ip, mac, _ = line_parts
                try:
                    host = socket.gethostbyaddr(ip)[0]
                except socket.herror:
                    host = "unknown"
                devices.append({"ip": ip, "mac": mac, "host": host})

        return devices
    except Exception as e:
        print(f"Error: {e}")


connected_devices = list_connected_devices()
for device in connected_devices:
    print(f"IP: {device['ip']}, MAC: {device['mac']}, Host: {device['host']}")


def send_http_request_to_devices(device_list):
    for device in device_list:
        hostname = device['host']
        if ".wlan" in hostname:
            hostname_no_wlan = hostname.replace(".wlan", "")
            hostname_local = f"{hostname_no_wlan}.local"
            url = f"http://{hostname_local}:5000/"
            try:
                response = requests.get(url, timeout=5)
                print(f"Response from {hostname_local}: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to {hostname_local}: {e}")


send_http_request_to_devices(connected_devices)