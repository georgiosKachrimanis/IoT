import math
from flask import *
from routes.status import *
from server import *
from revert_ap_client_mode import *
import json
import os
import time

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


def calcullate_next_AP():
    """
    Determines the next Access Point (AP) device based on the distances between all devices,
    and updates the status of the devices in the 'connected_devices.json' file.

    Returns:
        - True if the current device is still an AP
        - False if a new device has become an AP

    Raises:
        - ValueError: If the current device is not found in the 'connected_devices.json' file
        or if there is an error updating the file.
    """
    devices_totals = calculate_distances(extract_devices())
    sorted_totals = dict(sorted(devices_totals.items(), key=lambda item: item[1]))

    if sorted_totals:
        first_device_name = next(iter(sorted_totals.keys()))
        if first_device_name == local_host:
            print(f"The {local_host} is still AP, there will be no changes")
            return first_device_name
        else:
            print(f"The {first_device_name} will be the new AP+++++++++")
            # Update of the status of the new AP

            return first_device_name



def change_ap(new_ap):
    """
    Sends a request to the server of the specified device to change the access point (AP).

    Args:
        new_ap (str): The name of the device that will become the new AP.

    Returns:
        None: The function does not return anything.

    Raises:
        requests.exceptions.HTTPError: If the request to the server returns an error response.
        requests.exceptions.RequestException: If the request to the server fails for any other reason.
    """

    url = f'http://{new_ap}@{new_ap}:5000/revert_to_ap'
    requests.post(url)

    print("Now we have to change to client")
    revert_to_client_mode()


def update_device_data(device_name, is_ap):
    """
    Update the device data JSON file to set the "is_ap" value for the specified device.

    Args:
    - device_name (str): The name of the device to update.
    - is_ap (bool): The new value of the "is_ap" key.

    Raises:
    - FileNotFoundError: If the device data JSON file cannot be found.
    - ValueError: If the specified device name is not found in the JSON data.
    - KeyError: If the JSON data is not in the expected format.
    """
    # Load the device data JSON file
    file_path = f"/home/{local_host}/Desktop/code/data/connected_devices.json"
    try:
        with open(file_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Device data file '{file_path}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON data in file '{file_path}': {e}")

    # Update the "is_ap" value for the specified device

    for device in data:
        if device["name"] == device_name:
            device["is_ap"] = is_ap

            break
    else:
        raise ValueError(f"Device '{device_name}' not found in JSON data.")

    # Save the updated data back to the JSON file
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        raise ValueError(f"Error writing updated data to file '{file_path}': {e}")


def bandwidth_control():
    if status.bandwidth > 60:
        url = f'http://{local_host}@{local_host}:5000/camera_requests'
        send_command = {'function_name': 'camera', 'action': 'start'}

        # Send the request to the endpoint on the AP
        response = requests.post(url, json=send_command)
        # Check the status code of the response
        if response.status_code == 200:
            print(f'Request has the status {response.status_code}.')
        else:
            print(f'Request failed with status code {response.status_code}.')
    else:
        url = f'http://{local_host}@{local_host}:5000/camera_requests'
        send_command = {'function_name': 'camera', 'action': 'stop'}
        print(f"Bandwidth is {status.bandwidth}")
        # Send the request to the endpoint on the AP
        response = requests.post(url, json=send_command)
        # Check the status code of the response
        if response.status_code == 200:
            print('Request to STOP sent successfully.')
        else:
            print(f'Request failed with status code {response.status_code}.')

def count_down():
    seconds = 5

    while seconds > 0:
        print(seconds)
        time.sleep(1)
        seconds -= 1
