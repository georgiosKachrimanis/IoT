import socket
import subprocess
import psutil
import json
import random
import string
import requests

# Starting values of location and battery
coordinates = "A", 0
battery = 100


def is_rpi_ap():
    # Get the IP address of the Raspberry Pi's wlan0 interface
    cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    ip_address = subprocess.check_output(cmd, shell=True).decode().strip()

    # Check if the IP address ends with ".1"
    if ip_address.endswith('.1'):
        return True
    else:
        return False


def devices():
    # get the list of connected devices
    connected_devices = subprocess.check_output(['sudo', 'arp', '-a', '-i', 'wlan0']).decode().split('\n')

    # parse the list of devices to get the hostnames
    hostnames = [device.split()[0].split('.')[0] for device in connected_devices if len(device.split()) > 0]

    # filter hostnames starting with pixxx
    filtered_hostnames = [hostname for hostname in hostnames if hostname.startswith('pi')]

    # return the response to the client
    return filtered_hostnames


def disk_space():
    disk_usage = psutil.disk_usage('/')
    return disk_usage.free


def mem_usage():
    return psutil.virtual_memory()


def get_device_name():
    return socket.gethostname()


def new_coordinates():
    # Generate a random integer between 1 and 10 for the X coordinate
    y = random.randint(0, 9)
    # Generate a random uppercase letter between A and J for the Y coordinate
    x = random.choice(string.ascii_uppercase[0:10])
    return x, y


def new_battery():
    # Generate a random integer between 1 and 100 for the battery charge
    updated_battery = random.randint(1, 100)
    return updated_battery


def check_wifi_connection():
    try:
        subprocess.check_output(['iwgetid'])
        return True
    except subprocess.CalledProcessError:
        return False


def create_json_data_file():
    # Create a dictionary to hold the data
    data = {}

    hostname = get_device_name()

    # Get the available storage (in bytes)
    available_storage = disk_space()

    # Get the total memory and available memory (in bytes)
    mem = mem_usage()

    # Position variables
    lat, lon = coordinates

    # Store the information, the size of memory and storage is in MBytes
    data['name'] = hostname
    data['battery_percent'] = battery
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

def download():
    client_ips = devices()
    # get the server IP address and file path from the request form
    for i in client_ips:
        file_path = 'data/data.json'
        localhost = get_device_name()
        # construct the URL of the file on the remote server
        url = f'http://{i}@{i}.local:5000/download/{file_path}'
        # download the file and save it to the local file system
        file_name = file_path.split('/')[-1]
        local_file_path = f'/home/{localhost}/Desktop/code/data/{i}data.json'  # Remove the 'pi' prefix from i

        try:
            download_file(url, local_file_path)
            print(f"The data file from {i} is added.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file from {i}: {e}")

    # return a response to the client
    return 'Downloaded file(s) from server(s).'



def download_file(url, file_path):
    create_json_data_file()
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return file_path


def shutdown():
    subprocess.run(['sudo', 'shutdown', '-h', 'now'])
