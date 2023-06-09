import socket
from flask import *
from control_functions import *
from routes import camera_control
from revert_ap_client_mode import *
import requests

from werkzeug.utils import secure_filename

server = Flask(__name__)

hostname = socket.gethostname()
available = True
previous_state = ''


# # Start the libcamera-vid command as a separate process
# libcamera_process = subprocess.Popen(
#     ['libcamera-vid', '-t', '0', '--inline', '--listen', '-o', 'tcp://0.0.0.0:8000'],
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE
# )


# @server.route('/stream')
# def stream():
#     # Set the content type to multipart/x-mixed-replace
#     # to enable streaming in the browser
#     return Response(
#         libcamera_process.stdout,
#         mimetype='multipart/x-mixed-replace; boundary=FRAME'
#     )


@server.route('/stop_camera', methods=['POST', 'GET'])
def stop_camera_handler():
    """
    Stops the camera function.

    Args:
        None.

    Returns:
        A JSON object containing a success status message.
    """

    return camera_control.stop_camera()


@server.route('/start_camera', methods=['POST', 'GET'])
def start_camera_handler():
    """
    Starts the camera function.

    Args:
        None.

    Returns:
        A JSON object containing a success status message.
    """

    return camera_control.start_camera()


@server.route('/')
def home():
    """
    Renders the home page for the Flask app.

    Args:
        None.

    Returns:
        A rendered HTML template for the home page.
    """
    connected_devices_data = []
    if os.path.exists(f'/home/{hostname}/Desktop/netwiz/data/connected_devices.json'):
        with open(f'/home/{hostname}/Desktop/netwiz/data/connected_devices.json', 'r') as f:
            connected_devices_data = json.load(f)
    return render_template('index.html', devices_data=connected_devices_data)


@server.route('/download_file', methods=['POST'])
def download():
    """
    Downloads a file from a remote device and saves it to the local file system.

    Args:
        None.

    Returns:
        None.
    """
    download()


@server.route('/revert_to_ap', methods=['POST', 'GET'])
def revert_to_ap():
    """
    Reverts the device to Access Point (AP) mode.

    This function sends a request to revert the device to AP mode.
    It prints a message indicating the attempt to revert and calls the 'count_down' and 'revert_to_ap_mode' functions.

    Parameters:
    None

    Returns:
    None
    """
    count_down()
    revert_to_ap_mode()


def revert_to_client():
    """
    Reverts the device to Client mode.

    This function sends a request to revert the device to Client mode.
    It calls the 'revert_to_client_mode' function and returns a success message if the revert is successful,
    or an error message if an exception occurs.

    Parameters:
    None

    Returns:
    A string indicating the success message or error message.
    """

    try:
        revert_to_client_mode()
        return f'{hostname} successfully reverted to client mode.'
    except Exception as e:
        return f'Error: {str(e)}'


@server.route('/test/<path:url>', methods=['POST', 'GET'])
def send_request(url):
    """
    Sends an HTTP GET request to the specified URL and checks if the server is up.

    This function sends an HTTP GET request to the provided URL and checks if the server is up by verifying
    the response status netwiz. If the server is up, it returns a success message. Otherwise, it returns a failure message.

    Parameters:
    url (str): The URL to send the request to.

    Returns:
    A string indicating the success or failure message.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception if the response status netwiz is not successful
        return "Server is up and running."
    except requests.exceptions.RequestException as e:
        return f"Server is not available: {str(e)}"


@server.route('/download/<path:file_path>')
def serve_file(file_path):
    """
    Serves a file from the local file system.

    Args:
        file_path (str): The path to the file to serve.

    Returns:
        The requested file as an attachment.
    """
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)


@server.route('/receive-connected-devices', methods=['POST', 'GET'])
def receive_connected_devices():
    """
    Receives a file containing information about connected devices at the AP and saves it in the local machine.

    Returns:
    - (str): 'Success' if the file was successfully received and saved, 'Error' otherwise.
    """
    try:
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
            print(f"Received file '{filename}'")
            return 'Success'
        else:
            raise ValueError("No file received.")
    except Exception as e:
        print(f"Error receiving connected devices file: {e}")
        return 'Error'


@server.route('/end', methods=['GET'])
def end():
    """
    Shuts down the Server.

    Args:
        None.

    Returns:
        A message indicating that the server has been shut down.
    """
    return shutdown()


# @server.route('/update_bandwidth', methods=['POST', 'GET'])
# def update_bandwidth():
#     """
#     Updates the available bandwidth on the server.
#
#     Args:
#         None.
#
#     Returns:
#         A JSON object containing a success status message.
#     """
#
#     data_rate = request.get_json()
#     new_value = data_rate['new_value']
#     bandwidth = new_value
#     print(f"Updated value: {bandwidth}")
#     return jsonify({'success': True})

# @server.route('/data')
# def data():
#     """
#     Reads data from a JSON file and renders it on a web page.
#
#     Args:
#         None.
#
#     Returns:
#         A rendered HTML template containing the data from the JSON file.
#     """
#
#     # read the JSON file
#     with open(f'/home/{hostname}/Desktop/netwiz/data/data.json') as f:
#         information = json.load(f)
#
#     # render the data template with the data
#     return render_template('data.html', data=information)


# @server.route('/status/<hostname>', methods=['GET'])
# def server_status(user):
#     """
#     Retrieves the status of a specified server.
#
#     Args:
#         user (str): The name of the server to retrieve the status of.
#
#     Returns:
#         A rendered HTML template containing the status information of the specified server.
#     """
#
#     response = send_request('http://' + user + '.local:5000/')
#     return render_template('start_server.html', response=response)

#
# @server.route('/camera_handler', methods=['POST'])
# def camera_handler():
#     """
#     This function handles the 'start_camera' and 'stop_camera' messages received from
#     connected devices.
#
#     If the 'message' key in the request JSON is 'start_camera' and the previous state was
#     not 'start_camera', the function starts the camera functionality.
#     If the 'message' key is 'stop_camera' and the previous state was not 'stop_camera',
#     the function stops the camera functionality.
#     If the 'message' key is anything else, the function does nothing.
#
#     Args:
#         None.
#
#     Returns:
#         A JSON response with a 'success' key set to True.
#     """
#
#     received_command = request.get_json()
#     message = received_command['message']
#     global previous_state
#     if message == 'start_camera' and previous_state != message:
#         # Start the camera function and start broadcasting
#         print(f"Starting camera... the previous state was {previous_state}")
#         previous_state = message
#     elif message == 'start_broadcasting' and previous_state != message:
#         # Start again the broadcasting function
#         previous_state = message
#         print(f"Starting camera broadcasting... the previous state was {previous_state}")
#     elif message == 'stop_broadcasting' and previous_state != message:
#         # Stop broadcasting video
#         previous_state = message
#         print(f"Stop camera broadcasting... the previous state was {previous_state}")
#     elif message == 'stop_camera' and previous_state != message:
#         # Stop the broadcasting function
#         previous_state = message
#         print(f"Stopping camera... the previous state was {previous_state}")
#     else:
#         # I do not know what here will be... maybe stop in general the camera
#         print(f"Unknown message received and the previous state was {previous_state} ")
#
#     return jsonify({'success': True})

# @server.route('/update_device_mode', methods=['POST', 'GET'])
# def update_device_mode():
#
#     return jsonify({'message': 'Device mode updated'})

# @server.route('/camera_requests', methods=['GET', 'POST'])
# def camera():
#
#     clients = status.devices()
#     command = request.get_json()
#     success = False
#     if command['action'] == 'start':
#         message = {'message': 'start_camera'}
#     elif command['action'] == 'stop_broadcasting':
#         message = {'message': 'stop_broadcasting'}
#     elif command['action'] == 'start_broadcasting':
#         message = {'message': 'start_broadcasting'}
#     else:
#         message = {'message': 'no_change'}
#
#     for client in clients:
#         print(f'Trying to send request to connected device {client}')
#         url = f'http://{client}@{client}:5000/camera_handler'
#         server_url = f'http://{client}@{client}:5000/'
#         # Extra netwiz to avoid issues
#         if is_server_active(server_url):
#             response = requests.post(url, json=message)
#             if response.status_code == 200:
#                 print('Request sent successfully.')
#                 success = True
#             else:
#                 print(f'Request failed with status netwiz {response.status_code}.')
#         else:
#             print('Server not active.')
#
#     if success:
#         return jsonify({'success': True})
#     else:
#         return jsonify({'success': False})


# Start the server on all network interfaces
if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0')
