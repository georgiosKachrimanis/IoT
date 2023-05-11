from routes import status
from revert_ap_client_mode import *
import json


class Device:
    """
    A class representing a device.

    Attributes:
    - name (str): The name of the device.
    - position (dict): A dictionary containing the latitude and longitude of the device's position.
    - battery_percent (int): The percentage of battery life remaining for the device.
    - available_storage (float): The amount of available storage space on the device in gigabytes.
    - total_memory (float): The total amount of memory available on the device in gigabytes.
    - available_memory (float): The amount of available memory on the device in gigabytes.
    - is_ap (bool): A flag indicating whether or not the device is currently functioning as an access point.
    """

    def __init__(self):
        self.name = status.get_device_name()
        self.battery_percent = status.new_battery()
        self.available_storage = round(status.disk_space() / 1024 / 1024, 2)
        self.position = status.new_coordinates()  # or whichever function provides the location data
        self.is_ap = status.is_rpi_ap()
        self.mode = 'ap' if self.is_ap else 'client'

    def __str__(self):
        return f"Device Name: {self.name}" \
               f"\nAvailable Storage: {self.available_storage}" \
               f"\nBattery Percent: {self.battery_percent}" \
               f"\nPosition: {self.position}" \
               f"\nStatus: The {self.name} is {self.mode}"

    def is_ap(self):
        return self.is_ap

    def set_ap_status(self, new_status):
        """
        Sets the AP status of the device.

        Args:
            new_status (bool): True if the device is an AP, False otherwise.
        """
        self.is_ap = new_status

    def is_device_ap(self):
        """
        Returns True if the device is in access point (AP) mode, False otherwise.
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

    def set_mode(self, new_mode):
        """
        Sets the network mode for the device.
        Args:
            new_mode (str): The new network mode to set. Can be either "ap"
            for access point mode or "client" for client mode.
        Returns:
            None
        Raises:
            None
        Note:
            If the current mode is different than the new mode, the method will update the mode attribute
            and call the appropriate method to switch to the new mode.
            If the current mode is the same as the new mode, the method will
            print a message indicating that no changes were made to the network status.
        """
        if self.mode != new_mode:
            self.mode = new_mode
        else:
            print("No changes in network status")
