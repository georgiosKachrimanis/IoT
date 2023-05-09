import datetime
import socket
import subprocess
import psutil
import json
import random
import os
import requests


battery = 100
bandwidth = 100


def is_rpi_ap():
    """
    Check if the Raspberry Pi is currently acting as an access point.

    Returns:
        bool: True if the Pi is an access point, False otherwise.
    """
    # Get the IP address of the Raspberry Pi's wlan0 interface
    cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    ip_address = subprocess.check_output(cmd, shell=True).decode().strip()

    # Check if the IP address ends with ".1"
    if ip_address.endswith('.1'):
        return True
    else:
        return False


def devices():
    """
    Get a list of connected devices to the Raspberry Pi.

    Returns:
        list: A list of connected device hostnames.
    """
    # get the list of connected devices
    connected_devices = subprocess.check_output(['sudo', 'arp', '-a', '-i', 'wlan0']).decode().split('\n')

    # parse the list of devices to get the hostnames
    hostnames = [device.split()[0].split('.')[0] for device in connected_devices if len(device.split()) > 0]

    # filter hostnames starting with pixxx
    filtered_hostnames = [hostname for hostname in hostnames if hostname.startswith('pi')]

    # return the response to the client
    return filtered_hostnames


def is_server_active(url):
    """
    Check if a server is active by attempting to send a GET request to it.

    Args:
        url (str): The URL of the server to check.

    Returns:
        bool: True if the server is active, False otherwise.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f'server with {url} is active')
            return True
        else:
            return False
    except:
        return False


def disk_space():
    """
    Get the amount of available disk space on the Raspberry Pi.

    Returns:
        int: The amount of available disk space in bytes.
    """
    disk_usage = psutil.disk_usage('/')
    return disk_usage.free


def mem_usage():
    """
    Get the amount of available memory on the Raspberry Pi.

    Returns:
        tuple: A tuple containing the total and available memory in bytes.
    """
    return psutil.virtual_memory()


def get_device_name():
    """
    Get the hostname of the Raspberry Pi.

    Returns:
        str: The hostname of the Raspberry Pi.
    """
    return socket.gethostname()


def next_coordinates(device_list):
    """
    Generate a sequence of coordinates from a given list of coordinates.

    Args:
        device_list (list): A list of coordinates.

    Yields:
        tuple: A tuple containing the next set of coordinates from the list.
    """
    i = 0
    while True:
        yield device_list[i]
        i = (i + 1) % len(device_list)


def new_coordinates():
    """
    Generate a new set of coordinates for the Raspberry Pi based on its hostname.

    Returns:
        tuple: A tuple containing the latitude and longitude of the new coordinates.
    """
    name = get_device_name()
    if name not in generators:
        raise ValueError("Invalid device name")
    x, y = next(generators[name])
    return x, y


# Create a dictionary to hold the generator objects for each device
pi2 = [(1, 0), (2, 0), (2, -1), (4, 0), (5, -2), (3, -4), (0, -2), (0, -2), (-2, -1), (1, -1), (2, 0)]
pi3 = [(0, 1), (3, 0), (1, 2), (3, 2), (1, 3), (-1, 1), (-1, 1), (-4, 3), (-1, 5), (2, 3), (5, 1)]
pi4 = [(0, 0), (1, 0), (1, 0), (2, 0), (4, 1), (4, -1), (5, -5), (1, -5), (-1, -3), (1, -2), (-1, 0)]

generators = {"pi2": next_coordinates(pi2), "pi3": next_coordinates(pi3), "pi4": next_coordinates(pi4)}


def get_wifi_network():
    """
    Returns the name of the currently connected WiFi network.

    Returns:
    str: The name of the currently connected WiFi network.
    """
    # Run the iwconfig command and capture the output
    output = subprocess.check_output(['iwgetid', '-r'])

    # Convert the output to a string and remove any trailing newlines
    ssid = output.decode('utf-8').rstrip('\n')
    return ssid


def new_battery():
    """
    Returns a random integer between 1 and 100 to simulate battery level.

    Returns:
    int: A random integer between 1 and 100 to simulate battery level.
    """
    # Generate a random integer between 1 and 100 for the battery charge
    updated_battery = random.randint(1, 100)
    return updated_battery


def check_wifi_connection():
    """
    Checks if the Raspberry Pi is currently connected to a WiFi network.

    Returns:
    bool: True if the Raspberry Pi is connected to a WiFi network, False otherwise.
    """
    try:
        subprocess.check_output(['iwgetid'])
        return True
    except subprocess.CalledProcessError:
        return False


def create_json_data_file():
    """
    Creates a JSON data file with information about the Raspberry Pi, including its name, battery level,
    available storage, available memory, position, and whether or not it is an access point.

    Returns:
    str: The file path of the JSON data file that was created.
    """
    # Create a dictionary to hold the data
    data = {}

    hostname = get_device_name()

    # Get the available storage (in bytes)
    available_storage = disk_space()

    # Get the total memory and available memory (in bytes)
    mem = mem_usage()

    # Position variables
    lat, lon = new_coordinates()

    # Store the information, the size of memory and storage is in MBytes
    data['name'] = hostname
    data['time'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data['battery_percent'] = battery
    data['available_storage'] = round(available_storage / 1024 / 1024, 2)
    data['total_memory'] = round(mem.total / 1024 / 1024, 2)
    data['available_memory'] = round(mem.available / 1024 / 1024, 2)
    data['position'] = {'latitude': lat, 'longitude': lon}
    data['is_ap'] = is_rpi_ap()

    # Write the dictionary to the JSON file
    file_path = f'/home/{hostname}/Desktop/code/data/{hostname}data.json'  # <-- Add hostname to file path
    with open(file_path, 'w') as f:
        json.dump(data, f)

    # In order to avoid problems with write read rights
    os.chmod(file_path, 0o666)
    return file_path


def download():
    """
    Downloads the data files of connected Raspberry Pis from their respective servers, and saves them to the local machine.

    Returns:
    str: A message indicating whether the download was successful or not.
    """
    client_ips = devices()
    # get the server IP address and file path from the request form
    for i in client_ips:
        file_path = f'data/{i}data.json'
        localhost = get_device_name()
        # construct the URL of the file on the remote server
        server_url = f'http://{i}@{i}.local:5000/'

        if is_server_active(server_url):
            url = f'http://{i}@{i}.local:5000/download/{file_path}'
            local_file_path = f'/home/{localhost}/Desktop/code/data/{i}data.json'
            try:
                download_file(url, local_file_path)
                print(f"The data file from {i} is added.")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading file from {i}: {e}")
        else:
            print(f'The server on {i} is not reachable')

    # return a response to the client
    return 'Downloaded file(s) from server(s).'


def download_file(url, file_path):
    """
    Downloads a file from the given URL and saves it to the specified file path.

    Args:
        url (str): The URL to download the file from.
        file_path (str): The path to save the downloaded file.

    Returns:
        str: The path of the downloaded file.

    Raises:
        requests.exceptions.RequestException: If an error occurs while downloading the file.
    """
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    # In order to avoid problems with write read rights
    os.chmod(file_path, 0o666)
    return file_path


def shutdown():
    """
    Shuts down the Raspberry Pi.
    """
    subprocess.run(['sudo', 'shutdown', '-h', 'now'])
