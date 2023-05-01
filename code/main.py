# This process will run the main program of the whole project.
# It will start by activating the server.
#
import threading
import time

from server import *
from routes import status


def start_flask_app():
    if __name__ == '__main__':
        server.run(debug=True, host='0.0.0.0', use_reloader=False)


# Start the Flask app in a separate thread, this is to avoid issues of process not running.
flask_thread = threading.Thread(target=start_flask_app)
flask_thread.start()
print('Flask app is running!')
create_json_data_file()

# Available bandwidth with the cloud Server
bandwidth = 100

def main():
    while True:
        if is_rpi_ap():
            print("RPi is in AP mode")
            download()
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
