import requests
from flask import *
from .status import *
import json
import os

name = get_device_name()
connected_devices = devices()


def control_panel():
    filtered_hostnames = http_devices().split('<br>')[:-1]
    return render_template('index.html', filtered_hostnames=filtered_hostnames)


def http_devices():
    filtered_hostnames = devices()
    # create a response string with the hostnames of the connected devices
    response = "<h1>Connected Devices:</h1><br>"
    for hostname in filtered_hostnames:
        response += f"{hostname}<br>"

    # return the response to the client
    return response


def read_device_data(file_path):
    """
    Read the JSON data from a file and return a dictionary with the device data.
    :param file_path: the path to the file containing the device data.
    :return: a dictionary containing the device data.
    """
    with open(file_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data in file '{file_path}': {e}")
            return None

    return data


def create_devices_file():
    """
    Create a new JSON file with information about all connected devices, including the AP.
    :param devices_data: a list of dictionaries with information about each device, containing the following keys:
                         - 'hostname': the hostname of the device
                         - 'location': the location of the device
                         - 'battery': the remaining battery of the device
    """
    folder_path = f'/home/{name}/Desktop/code/data'
    devices_data = []
    for file_name in os.listdir(folder_path):

        if file_name.endswith('data.json'):
            file_path = os.path.join(folder_path, file_name)
            devices_data.append(read_device_data(file_path))

    filename = f'/home/{name}/Desktop/code/data/connected_devices.json'
    with open(filename, 'w') as f:
        json.dump(devices_data, f)


def receive_connected_devices():

    access_point = get_wifi_network()
    server_url = f'http://{access_point}@{access_point}.local:5000/'
    file_path = '/data/connected_devices.json'

    if is_server_active(server_url):
        url = f'{server_url}download/{file_path}'
        local_file_path = f'/home/{name}/Desktop/code/data/connected_devices.json'
        try:
            download_file(url, local_file_path)
            print(f"The data file from {access_point} is added.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file from {access_point}: {e}")
    else:
        print(f'The server on {access_point} is not reachable')



