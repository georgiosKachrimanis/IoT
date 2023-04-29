# This process will run the main program of the whole project.
# It will start by activating the server.
#
import threading
from server import *
from routes.status import *
from routes.control_panel import *


def start_flask_app():

    if __name__ == '__main__':
        server.run(debug=True, host='0.0.0.0', use_reloader=False)


# Start the Flask app in a separate thread, this is to avoid issues of process not running.
flask_thread = threading.Thread(target=start_flask_app)
flask_thread.start()


print('Flask app is running!')
create_json_data_file()

# with server.test_client() as client:
#     response = client.get('/data')
#     result = response.data.decode('utf-8')
#     print(result)


if is_rpi_ap():
    filtered_hostnames = devices()
    print(filtered_hostnames)
    print("*"*20)
    download()


