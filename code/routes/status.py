import socket
import subprocess
import psutil
import json


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
    hostname = get_device_name()

    # get the available memory in bytes and convert to MB
    mem = psutil.virtual_memory().available / 1024 / 1024

    # check if the device is acting as an access point
    is_ap = is_rpi_ap()

    # create a response string
    response = f"Device Name: {hostname}\nAvailable Memory: {mem:.2f} MB\nIs AP: {is_ap}"

    return response


def disk_space():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.free


def mem_usage():
    return psutil.virtual_memory()


def get_device_name():
    return socket.gethostname()


def coordinates():
    x = "X"
    y = 52
    return x, y


def get_battery():
    battery = 35
    return battery


def create_json_data_file():
    # Create a dictionary to hold the data
    data = {}

    hostname = get_device_name()

    # Get the available storage (in bytes)
    available_storage = disk_space()

    # Get the total memory and available memory (in bytes)
    mem = mem_usage()

    # Position variables
    lat, lon = coordinates()

    # Store the information, the size of memory and storage is in MBytes
    data['name'] = hostname
    data['battery_percent'] = get_battery()
    data['available_storage'] = round(available_storage / 1024 / 1024, 2)
    data['total_memory'] = round(mem.total / 1024 / 1024, 2)
    data['available_memory'] = round(mem.available / 1024 / 1024, 2)
    data['position'] = {'latitude': lat, 'longitude': lon}
    data['is_ap'] = is_rpi_ap()

    # Write the dictionary to the JSON file
    # The file_path is to avoid problems with the installation
    file_path = '/home/' + hostname + '/Desktop/code/data/data.json'
    with open(file_path, 'w') as f:
        json.dump(data, f)

    return file_path



def shutdown():
    subprocess.run(['sudo', 'shutdown', '-h', 'now'])
