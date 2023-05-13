
from Device import Device
from server import *
from control_functions import *


# local_host = get_device_name()
# Create an instance of the Device
local_device = Device()


def main():
    print("Welcome traveler!!!")
    time.sleep(10)
    while True:

        # Create a json file of the local device
        create_json_data_file()
        router_status = is_rpi_ap()

        print(f"STATUS DEVICE IS {local_device.mode} and the router is in {router_status}")
        # check the status of the device and act accordingly
        if is_rpi_ap():
            # Timer in order to wait for the rest of the devices to catch up
            time.sleep(10)
            print(f"{local_device.name} is in AP mode")
            # Get the data of the connected devices
            download()
            # Create the data for the connected devices
            create_devices_file()
            # Calculate which device should be AP
            calculate_next_AP()
            print(f"The new AP is calculated")
            time.sleep(10)
            print('Now we wait 10 seconds before the final check')

        elif check_wifi_connection():
            print(f"{local_device.name} is connected to {get_wifi_network()} and we have to wait for 10 seconds")

            # In order to be sure that the AP have processed the data
            time.sleep(20)
            receive_connected_devices()
            print(f"Connected devices are received this is  {local_device.name} we are going now for the final check")

        else:
            print("Rpi is in another state.\n Please HELP!!!")
            # Here will check if the connected devices file exists and then create check the order
            time.sleep(20)
        print(f"Status BEFORE updates --> \ndevice mode = {local_device.mode}\nrouter_mode = {router_status}")
        # Now we ask the devices to update their status
        local_device.update_device_modes()
        print(f"Status AFTER update--> \ndevice mode = {local_device.mode}\nrouter_mode = {router_status}")

        if router_status and local_device.mode == 'client':
            print(f"The {local_device.name} will revert to client mode in:")
            count_down()
            revert_to_client_mode()
        if not router_status and local_device.mode == 'ap':
            print(f"The {local_device.name} will revert to client mode in:")
            count_down()
            revert_to_ap_mode()

        # I will allow one-minute timer because there were some issues between changes of networks
        time.sleep(60)


main()
