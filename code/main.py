# This process will run the main program of the whole project.
# It will start by activating the server.
#
import threading
import time

from server import *
from routes import status
from routes.status import *


def start_flask_app():
    if __name__ == '__main__':
        server.run(debug=True, host='0.0.0.0', use_reloader=False)


# Start the Flask app in a separate thread, this is to avoid issues of process not running.
flask_thread = threading.Thread(target=start_flask_app)
flask_thread.start()
print('Flask app is running!')
create_json_data_file()
local_host = get_device_name()
# Available bandwidth with the cloud Server



def main():
    while True:
        print(f'inside the main and while true {status.bandwidth}')
        if is_rpi_ap():
            print("RPi is in AP mode")
            download()
            if status.bandwidth > 50:
                url = f'http://{local_host}@{local_host}:5000/camera'
                data = {'function_name': 'camera', 'action': 'start'}
                print(f"Bandwidth is {status.bandwidth}")
                # Send the request to the endpoint on the AP
                response = requests.post(url, json=data)
                # Check the status code of the response
                if response.status_code == 200:
                    print('Request sent successfully.')
                else:
                    print(f'Request failed with status code {response.status_code}.')
            else:
                url = f'http://{local_host}@{local_host}:5000/camera'
                data = {'function_name': 'camera', 'action': 'stop'}
                print(f"Bandwidth is {status.bandwidth}")
                # Send the request to the endpoint on the AP
                response = requests.post(url, json=data)
                # Check the status code of the response
                if response.status_code == 200:
                    print('Request to STOP sent successfully.')
                else:
                    print(f'Request failed with status code {response.status_code}.')


        elif check_wifi_connection():
            print("Rpi is connected to a known network")
        else:
            print("Rpi is in another state.")
        time.sleep(60)


# with server.test_client() as client:
#     response = client.get('/data')
#     result = response.data.decode('utf-8')
#     print(result)

# AP_status = is_rpi_ap()
#
# while AP_status:
#     time.sleep(60)
#     filtered_hostnames = devices()
#     print(filtered_hostnames)
#     print("*"*20)
#     download()
#

main()
