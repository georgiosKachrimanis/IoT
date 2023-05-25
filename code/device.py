import datetime
import socket
import subprocess
import psutil
import json
import random
import os
import requests


class Device:
    """
    A class representing a device.

    Attributes:
        name (str): The name of the device.
        position (dict): A dictionary containing the latitude and longitude of the device's position.
        battery_percent (int): The percentage of battery life remaining for the device.
        available_storage (float): The amount of available storage space on the device in gigabytes.
        mode (str): A flag indicating whether or not the device is currently functioning as an access point.

    Methods:
        __init__(): Initializes a new instance of the Device class.
        __str__(): Returns a string representation of the Device object.
        is_device_ap(): Checks if the device is in access point (AP) mode.
        read_data_file(): Reads the JSON data file containing information about connected devices.
        update_device_modes(): Updates the device's network mode based on the JSON data file.
        is_rpi_ap(): Checks if the Raspberry Pi is currently acting as an access point.
        devices(): Get a list of connected devices to the Raspberry Pi.
        is_server_active(): Check if a server is active by attempting to send a GET request to it.
        disk_space(): Get the amount of available disk space on the Raspberry Pi.
        mem_usage(): Get the amount of available memory on the Raspberry Pi.
        get_device_name(): Get the hostname of the Raspberry Pi.
        next_coordinates(): Generate a sequence of coordinates from a given list of coordinates.
        new_coordinates(): Generate a new set of coordinates for the Raspberry Pi based on its hostname.
        get_wifi_network(): Returns the name of the currently connected WiFi network.
        new_battery(): Returns a random integer between 1 and 100 to simulate battery level.
        check_wifi_connection(): Checks if the Raspberry Pi is currently connected to a WiFi network.
        create_json_data_file(): Creates a JSON data file with information about the Raspberry Pi.

    """
    def __init__(self):
        """
        Initializes a new instance of the Device class.

        Returns:
            None
        """
        self.name = self.get_device_name()
        self.battery_percent = self.new_battery()
        self.available_storage = round(self.disk_space() / 1024 / 1024, 2)
        self.position = self.new_coordinates()
        self.mode = 'ap' if self.is_rpi_ap() else 'client'

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
        file_path = f"/home/{self.name}/Desktop/code/data/connected_devices.json"
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Convert the list to a dictionary using the device name as key
        data_dict = {device['name']: device for device in data}
        return data_dict

    def update_device_modes(self):
        """
        Updates the device's network mode based on the JSON data file.

        Returns:
            None
        """
        filename = f'/home/{self.name}/Desktop/code/data/connected_devices.json'
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def disk_space():
        """
        Get the amount of available disk space on the Raspberry Pi.

        Returns:
            int: The amount of available disk space in bytes.
        """
        disk_usage = psutil.disk_usage('/')
        return disk_usage.free

    @staticmethod
    def mem_usage():
        """
        Get the amount of available memory on the Raspberry Pi.

        Returns:
            tuple: A tuple containing the total and available memory in bytes.
        """
        return psutil.virtual_memory()

    @staticmethod
    def get_device_name():
        """
        Get the hostname of the Raspberry Pi.

        Returns:
            str: The hostname of the Raspberry Pi.
        """
        return socket.gethostname()

    @staticmethod
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

    def new_coordinates(self):
        """
        Generate a new set of coordinates for the Raspberry Pi based on its hostname.

        Returns:
            tuple: A tuple containing the latitude and longitude of the new coordinates.
        """
        name = self.get_device_name()
        if name not in generators:
            raise ValueError("Invalid device name")
        x, y = next(generators[name])
        return x, y

    @staticmethod
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

    @staticmethod
    def new_battery():
        """
        Returns a random integer between 1 and 100 to simulate battery level.

        Returns:
            int: A random integer between 1 and 100 to simulate battery level.
        """
        # Generate a random integer between 1 and 100 for the battery charge
        updated_battery = random.randint(1, 100)
        return updated_battery

    @staticmethod
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

    @staticmethod
    def create_json_data_file():
        """
        Creates a JSON data file with information about the Raspberry Pi, including its name, battery level,
        available storage, available memory, position, and whether or not it is an access point.

        Returns:
            str: The file path of the JSON data file that was created.
        """
        # Create a dictionary to hold the data
        data = {}

        hostname = Device.get_device_name()

        # Get the available storage (in bytes)
        available_storage = Device.disk_space()

        # Get the total memory and available memory (in bytes)
        mem = Device.mem_usage()

        # Position variables
        lat, lon = Device.new_coordinates()

        # Store the information, the size of memory and storage is in MBytes
        data['name'] = hostname
        data['time'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        data['battery_percent'] = Device.new_battery()
        data['available_storage'] = round(available_storage / 1024 / 1024, 2)
        data['total_memory'] = round(mem.total / 1024 / 1024, 2)
        data['available_memory'] = round(mem.available / 1024 / 1024, 2)
        data['position'] = {'latitude': lat, 'longitude': lon}
        data['is_ap'] = Device.is_rpi_ap()

        # Write the dictionary to the JSON file
        file_path = f'/home/{hostname}/Desktop/code/data/{hostname}data.json'  # <-- Add hostname to file path
        with open(file_path, 'w') as f:
            json.dump(data, f)

        # In order to avoid problems with write read rights
        os.chmod(file_path, 0o666)
        return file_path
