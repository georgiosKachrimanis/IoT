import psutil
import socket
import subprocess
import random
import datetime
from control_functions import *

battery = 100
bandwidth = 100


class Device:
    """
    A class representing a device.

    Attributes:
        name (str): The name of the device.
        position (dict): A dictionary containing the latitude and longitude of the device's position.
        battery_percent (int): The percentage of battery life remaining for the device.
        available_storage (float): The amount of available storage space on the device in gigabytes.
        mode (str): A flag indicating whether the device is currently functioning as an access point.

    Methods:
        __init__(): Initializes a new instance of the Device class.
        __str__(): Returns a string representation of the Device object.
        is_device_ap(): Checks if the device is in access point (AP) mode.
        read_data_file(): Read the JSON data file containing information about connected devices.
        update_device_modes(): Updates the device's network mode based on the JSON data file.
    """

    def __init__(self):
        """
        Initializes a new instance of the Device class.

        Returns:
            None
        """
        self.name = get_device_name()
        self.battery_percent = new_battery()
        self.available_storage = round(disk_space() / 1024 / 1024, 2)
        self.position = new_coordinates()  # or whichever function provides the location data
        self.mode = 'ap' if is_rpi_ap() else 'client'

    def __str__(self):
        """
        Returns a string representation of the Device object.

        Returns:
            A string representation of the Device object.
        """
        return f"Device Name: {self.name}" \
               f"\nAvailable Storage: {self.available_storage}" \
               f"\nBattery Percent: {self.battery_percent}" \
               f"\nPosition: {self.position}" \
               f"\nStatus: The {self.name} is {self.mode}"

    def is_device_ap(self):
        """
        Checks if the device is in access point (AP) mode.

        Returns:
            True if the device is in AP mode, False otherwise.
        """
        data = self.read_data_file()
        if self.name in data:
            return data[self.name]['is_ap']
        else:
            return False

    def read_data_file(self):
        """
        Reads the JSON data file containing information about connected devices
        and returns a dictionary with device names as keys.
        Returns:
            A dictionary containing information about connected devices with device names as keys.
        """
        file_path = f"/home/{self.name}/Desktop/netwiz/data/connected_devices.json"
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Convert the list to a dictionary using the device name as a key
        data_dict = {device['name']: device for device in data}
        return data_dict

    def check_and_revert_mode(self):
        """
        Checks the router status and reverts the device's mode accordingly.

        Returns:
            None
        """
        router_status = is_rpi_ap()
        if router_status and self.mode == 'client':
            print(f"The {self.name} will revert to client mode in:")
            count_down()
            revert_to_client_mode()
        elif not router_status and self.mode == 'ap':
            print(f"The {self.name} will revert to client mode in:")
            count_down()
            revert_to_ap_mode()

    def update_device_modes(self):
        """
        Updates the device's network mode based on the JSON data file.

        Returns:
            None
        """
        filename = f'/home/{self.name}/Desktop/netwiz/data/connected_devices.json'
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            return
        except json.JSONDecodeError:
            print(f"Error decoding JSON data from file '{filename}'.")
            return

        for item in data:
            if item['name'] == self.name:
                is_ap = item.get('is_ap', False)
                self.mode = 'ap' if is_ap else 'client'
                break
        else:
            print(f"No matching device found with name '{self.name}' in the JSON data.")


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
    active_devices = subprocess.check_output(['sudo', 'arp', '-a', '-i', 'wlan0']).decode().split('\n')

    # parse the list of devices to get the hostnames
    hostnames = [device.split()[0].split('.')[0] for device in active_devices if len(device.split()) > 0]

    # filter hostnames starting with pixxx
    filtered_hostnames = [pi for pi in hostnames if pi.startswith('pi')]

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
            print(f'Server at {url} is active.')
            return True
        else:
            print(f'Server at {url} is not active. Status code: {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'Error occurred while checking server at {url}: {e}')
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
    Returns the name of the currently connected Wi-Fi network.

    Returns:
    str: The name of the currently connected Wi-Fi network.
    """
    # Run the iwconfig command and capture the output
    output = subprocess.check_output(['iwgetid', '-r'])

    # Convert the output to a string and remove any trailing newlines
    ssid = output.decode('utf-8').rstrip('\n')
    return ssid


def new_battery():
    """
    Using the global battery and retracting a random integer between 1 and 10 to simulate battery level.

    Returns:
    int: A new simulated battery level.
    """
    # Generate a random integer between 1 and 100 for the battery charge
    global battery
    random_battery_usage = random.randint(1, 10)
    updated_battery = battery - random_battery_usage
    battery = updated_battery
    return battery


def check_wifi_connection():
    """
    Checks if the Raspberry Pi is currently connected to a Wi-Fi network.

    Returns:
    bool: True if the Raspberry Pi is connected to a Wi-Fi network, False otherwise.
    """
    try:
        subprocess.check_output(['iwgetid'])
        return True
    except subprocess.CalledProcessError:
        return False


def create_json_data_file():
    """
    Creates a JSON data file with information about the Raspberry Pi, including its name, battery level,
    available storage, available memory, position, and whether it is an access point.

    Returns:
    str: The file path of the JSON data file that was created.
    """
    # Create a dictionary to hold the data
    data = {}

    pi = get_device_name()

    # Get the available storage (in bytes)
    available_storage = disk_space()

    # Get the total memory and available memory (in bytes)
    mem = mem_usage()

    # Position variables
    lat, lon = new_coordinates()

    # Store the information, the size of memory and storage is in MBytes
    data['name'] = pi
    data['time'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data['battery_percent'] = new_battery()
    data['available_storage'] = round(available_storage / 1024 / 1024, 2)
    data['total_memory'] = round(mem.total / 1024 / 1024, 2)
    data['available_memory'] = round(mem.available / 1024 / 1024, 2)
    data['position'] = {'latitude': lat, 'longitude': lon}
    data['is_ap'] = is_rpi_ap()

    # Write the dictionary to the JSON file
    file_path = f'/home/{pi}/Desktop/netwiz/data/{pi}data.json'  # <-- Add hostname to file path
    with open(file_path, 'w') as f:
        json.dump(data, f)

    # In order to avoid problems with write read rights
    os.chmod(file_path, 0o666)
    return file_path

    # def set_mode(self, new_mode):
    #     """
    #     Sets the network mode for the device.
    #     Args:
    #         new_mode (str): The new network mode to set. It Can be either "ap"
    #         for access point mode or "client" for client mode.
    #     Returns:
    #         None
    #     Raises:
    #         None
    #     Note:
    #         If the current mode is different from the new mode, the method will update the mode attribute
    #         and call the appropriate method to switch to the new mode.
    #         If the current mode is the same as the new mode, the method will
    #         print a message indicating that no changes were made to the network status.
    #     """
    #     if self.mode != new_mode:
    #         self.mode = new_mode
    #     else:
    #         print("No changes in network status")
