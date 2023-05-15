from routes import status
from revert_ap_client_mode import *
import json


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
    """
    def __init__(self):
        """
        Initializes a new instance of the Device class.

        Returns:
            None
        """
        self.name = status.get_device_name()
        self.battery_percent = status.new_battery()
        self.available_storage = round(status.disk_space() / 1024 / 1024, 2)
        self.position = status.new_coordinates()  # or whichever function provides the location data
        self.mode = 'ap' if status.is_rpi_ap() else 'client'

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



   # def set_mode(self, new_mode):
    #     """
    #     Sets the network mode for the device.
    #     Args:
    #         new_mode (str): The new network mode to set. Can be either "ap"
    #         for access point mode or "client" for client mode.
    #     Returns:
    #         None
    #     Raises:
    #         None
    #     Note:
    #         If the current mode is different than the new mode, the method will update the mode attribute
    #         and call the appropriate method to switch to the new mode.
    #         If the current mode is the same as the new mode, the method will
    #         print a message indicating that no changes were made to the network status.
    #     """
    #     if self.mode != new_mode:
    #         self.mode = new_mode
    #     else:
    #         print("No changes in network status")
