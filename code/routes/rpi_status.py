import socket
import subprocess
import psutil


def is_rpi_ap():
    # Get the IP address of the Raspberry Pi's wlan0 interface
    cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    ip_address = subprocess.check_output(cmd, shell=True).decode().strip()

    # Check if the IP address ends with ".1"
    if ip_address.endswith('.1'):
        return True
    else:
        return False


def device_status():
    # get the name of the device
    hostname = socket.gethostname()

    # get the available memory in bytes and convert to MB
    mem = psutil.virtual_memory().available / 1024 / 1024

    # check if the device is acting as an access point
    is_ap = is_rpi_ap()

    # create a response string
    response = f"Device Name: {hostname}\nAvailable Memory: {mem:.2f} MB\nIs AP: {is_ap}"

    return response


def shutdown():
    subprocess.run(['sudo', 'shutdown', '-h', 'now'])