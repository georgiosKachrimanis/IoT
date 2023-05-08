import math
from flask import *
from .status import *
import json
import os

local_host = get_device_name()
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
    folder_path = f'/home/{local_host}/Desktop/code/data'
    devices_data = []
    for file_name in os.listdir(folder_path):

        if file_name.endswith('data.json'):
            file_path = os.path.join(folder_path, file_name)
            devices_data.append(read_device_data(file_path))

    filename = f'/home/{local_host}/Desktop/code/data/connected_devices.json'
    with open(filename, 'w') as f:
        json.dump(devices_data, f)


def receive_connected_devices():

    access_point = get_wifi_network()
    server_url = f'http://{access_point}@{access_point}.local:5000/'
    file_path = '/data/connected_devices.json'

    if is_server_active(server_url):
        url = f'{server_url}download/{file_path}'
        local_file_path = f'/home/{local_host}/Desktop/code/data/connected_devices.json'
        try:
            download_file(url, local_file_path)
            print(f"The data file from {access_point} is added.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file from {access_point}: {e}")
    else:
        print(f'The server on {access_point} is not reachable')


def validate_points(points):
    """
    Validates a list of points to ensure that each point is a dictionary with a single name-coordinate pair.

    :param points: a list of dictionaries where each dictionary represents a device and contains the device name and its position.
    :return: a list of tuples where each tuple represents a device and contains the device name and its position.
    """
    validated_points = []
    for point in points:
        if len(point) != 2:
            raise ValueError("Invalid input: each point must be a dictionary with a single name-coordinate pair")
        name = point["name"]
        position = point["position"]
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Invalid input: position must be a tuple of two coordinates")
        validated_points.append((name, position))
    return validated_points


def calculate_distances(coordinates):
    """
    Calculates the distances between each pair of points and returns the total distance
    for each point.

    Args:
    - coordinates (list): A list of dictionaries, where each dictionary has a single
      name-coordinate pair. The name must be a string and the coordinate must be
      a tuple of two integers.

    Returns:
    - A dictionary of point names and their total distance from all other points.

    Raises:
    - ValueError: If the input points are not a non-empty list of dictionaries, or
      if any of the dictionaries have more or less than one key-value pair, or if
      the name or coordinate is not in the correct format.
    """
    validate_points(coordinates)

    n = len(coordinates)
    distances = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        name1 = coordinates[i]["name"]
        x1, y1 = coordinates[i]["position"]
        for j in range(i + 1, n):
            name2 = coordinates[j]["name"]
            x2, y2 = coordinates[j]["position"]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            distance = math.sqrt(dx * dx + dy * dy)
            distances[i][j] = distance
            distances[j][i] = distance

    totals = {}
    for i in range(n):
        device_name = coordinates[i]["name"]
        row_total = sum(distances[i])
        if device_name != "Center":
            totals[device_name] = row_total

    return totals


def sort_ascending(devices_dictionary):
    """
    Sorts the totals dictionary in ascending order by value and returns a list of tuples.

    Args:
    - totals (dict): A dictionary of point names and their total distance from all other points.

    Returns:
    - A list of tuples, where each tuple contains a point name and its corresponding total distance.
    """
    sorted_dict = sorted(devices_dictionary.items(), key=lambda x: x[1])
    return sorted_dict


def extract_devices():
    """
    Extracts the device name and position from a JSON file and returns them as a list of dictionaries.
    :param file_path: the path to the JSON file containing the device data.
    :return: a list of dictionaries where each dictionary represents a device and contains the device name and its position.
    """

    file_path = f'/home/{local_host}/Desktop/code/data/connected_devices.json'
    with open(file_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data in file '{file_path}': {e}")
            return None

    devices_dictionary = [{"name": "Center", "position": (0, 0)}]
    for device in data:
        device_name = device["name"]
        position = device["position"]
        latitude = position["latitude"]
        longitude = position["longitude"]
        devices_dictionary.append({"name": device_name, "position": (latitude, longitude)})

    return devices_dictionary


def check_next_AP():
    devices = extract_devices()
    devices_totals = calculate_distances(devices)
    sorted_totals = dict(sorted(devices_totals.items(), key=lambda item: item[1]))
    print(sorted_totals)

    if sorted_totals:
        first_device_name = next(iter(sorted_totals.keys()))
        print(first_device_name)
        if first_device_name == local_host:
            print(f"The {local_host} is also the {first_device_name}")
            return True
        else:
            print(f"The new AP is {first_device_name}")
            return False
