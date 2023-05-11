# This process will run the main program of the whole project.
# It will start by activating the server.
#
import threading
import time
from Device import Device

from server import *
from routes import status
from control_functions import *


def start_flask_app():
    if __name__ == '__main__':
        server.run(debug=True, host='0.0.0.0', use_reloader=False)


# Start the Flask app in a separate thread, this is to avoid issues of process not running.
flask_thread = threading.Thread(target=start_flask_app)
flask_thread.start()
print('Flask app is running!')
local_host = get_device_name()


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


def main():
    # Create an instance of the Device
    local_device = Device()
    count = 0
    while True:
        # Create a json file of the local device
        create_json_data_file()

        # check the status of the device and act accordingly
        if local_device.mode == 'ap':
            print(f"{local_device.name} is in AP mode")
            # Get the data of the connected devices
            download()
            # Create the data for the connected devices
            create_devices_file()
            # Calculate which device should be AP
            check_next_AP()
            print(f"The new AP is calculated")
            # wait some time so all the devices can ge the data
            time.sleep(15)
        elif check_wifi_connection():
            print(f"{local_device.name} is connected to {get_wifi_network()}")
            # In order to be sure that the AP have processed the data
            time.sleep(15)
            receive_connected_devices()
            print("Connected devices are received this is " + local_device.name)
        else:
            # Here we will create the commands to stop broadcasting and try to create a new AP
            # (If we have time we can also check the option to return to another network)
            count += 1
            print("Rpi is in another state.")
            if count % 2 == 0:
                local_device.set_mode('ap')

        if local_device.is_device_ap():
            print(f"Start now! \n{local_device} is AP++++++++++++++++++")
            local_device.set_mode('ap')

        else:
            print(f"We are at the last if else \n{local_device} is CLIENT-----------------------------")
            local_device.set_mode('client')

        if local_device.mode == 'ap' and local_device.is_ap:
            print("no changes")
        elif local_device.mode == 'client' and local_device.is_ap:
            revert_to_client_mode()
        elif local_device.mode == 'client' and not local_device.is_ap:
            print("no changes")
        else:
            revert_to_ap_mode()

        time.sleep(45)

main()
