# This process will run the main program of the whole project.
# It will start by activating the server.
#
import threading
import time

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

    while True:
        create_json_data_file()
        if is_rpi_ap():
            print(f"RPi {hostname} is in AP mode")
            # Get the data of the connected devices
            download()
            # Create the data for the connected devices
            create_devices_file()
            # Calculate if the device should be AP
            check_next_AP()
            time.sleep(15)  # To keep up with the clients

        elif check_wifi_connection():

            time.sleep(15)  # In order to be sure that the AP have processed the data
            receive_connected_devices()
            # Here we will create the commands to check start the camera automatically
            print(f"Rpi {hostname} is connected to {get_wifi_network()}")
        else:
            # Here we will create the commands to stop broadcasting and try to create a new AP
            # (If we have time we can also check the option to return to another network)
            print("Rpi is in another state.")
        time.sleep(45)


main()
