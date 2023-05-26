
from device import *
from server import *
from control_functions import *

# Create an instance of the Device
local_device = Device()


def main():
    # Control text, can be removed.
    print("The program had started!!!")
    time.sleep(10)
    counter = 0
    while True:
        # Create a json file of the local device
        create_json_data_file()
        router_status = is_rpi_ap()
        # Control text, can be removed.
        print(f"STATUS DEVICE IS {local_device.mode} and the router is in {router_status}")
        # check the status of the device and act accordingly
        if is_rpi_ap():
            # Timer to help synchronize devices
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

        elif check_wifi_connection():
            # Control text, can be removed.
            print(f"{local_device.name} is connected to {get_wifi_network()} and we have to wait for 10 seconds")
            # In order to be sure that the AP have processed the data
            time.sleep(20)
            # Receive the file with all the devices
            receive_connected_devices()
            # Control text, can be removed.
            print(f"Connected devices are received this is  {local_device.name} we are going now for the final check")

        else:
            print("Rpi is in another state.")
            # Adding +1 in the counter so after 2 cycles or 4 cycles we can go in the new AP
            counter += 1
            if counter == 2:
                # We are using a method to check if the device is the 2nd in line for AP and update the staus if it is.
                calculate_2nd_AP()
                counter = 0  # reset counter
            elif counter == 4:
                # If the 4th cycle comes and not an AP is available then the device will take over.
                update_device_data(local_device.name, 'is_ap')
                counter = 0  # reset counter
            time.sleep(20)

        # Control text, can be removed.
        print(f"Status BEFORE updates --> \ndevice mode = {local_device.mode}\nrouter_mode = {router_status}")
        # Now we ask the devices to update their status
        local_device.update_device_modes()
        print(f"Status AFTER update--> \ndevice mode = {local_device.mode}\nrouter_mode = {router_status}")

        local_device.check_and_revert_mode()
        # if router_status and local_device.mode == 'client':
        #     print(f"The {local_device.name} will revert to client mode in:")
        #     count_down()
        #     revert_to_client_mode()
        # if not router_status and local_device.mode == 'ap':
        #     print(f"The {local_device.name} will revert to client mode in:")
        #     count_down()
        #     revert_to_ap_mode()

        # Now the devices will start connecting to the new AP and will continue working as usual.
        time.sleep(60)


main()
