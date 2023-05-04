from flask import *
import io
import svgwrite
from routes import status
from routes.camera_control import start_camera, stop_camera
from routes.server_control import start_server
from routes.status import *
import requests

server = Flask(__name__)
status.create_json_data_file()
hostname = status.get_device_name()
available = True
previous_state = ''


@server.route('/camera', methods=['GET', 'POST'])
def camera():

    clients = status.devices()
    command = request.get_json()
    success = False
    if command['action'] == 'start':
        message = {'message': 'start_camera'}
    elif command['action'] == 'stop':
        message = {'message': 'stop_broadcasting'}
    else:
        message = {'message': 'No Idea'}

    for client in clients:
        print(f'Trying to send request to connected device {client}')
        url = f'http://{client}@{client}:5000/camera_controls'
        server_url = f'http://{client}@{client}:5000/'
        # Extra code to avoid issues
        if is_server_active(server_url):
            response = requests.post(url, json=message)
            if response.status_code == 200:
                print('Request sent successfully.')
                success = True
            else:
                print(f'Request failed with status code {response.status_code}.')
        else:
            print('Server not active.')

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@server.route('/connected')
def http_devices():
    return http_devices()


@server.route('/camera_controls', methods=['POST'])
def camera_handler():
    """
    This function handles the 'start_camera' and 'stop_camera' messages received from
    connected devices.

    If the 'message' key in the request JSON is 'start_camera' and the previous state was
    not 'start_camera', the function starts the camera functionality.
    If the 'message' key is 'stop_camera' and the previous state was not 'stop_camera',
    the function stops the camera functionality.
    If the 'message' key is anything else, the function does nothing.

    Args:
        None.

    Returns:
        A JSON response with a 'success' key set to True.
    """

    received_command = request.get_json()
    message = received_command['message']
    global previous_state
    if message == 'start_camera' and previous_state != message:
        # Start the camera function and start broadcasting
        print(f"Starting camera... the previous state was {previous_state}")
        previous_state = message
    elif message == 'stop_camera' and previous_state != message:
        # Stop the broadcasting function
        previous_state = message
        print(f"Stopping camera... the previous state was {previous_state}")
    else:
        # I do not know what here will be... maybe stop in general the camera
        print(f"Unknown message received and the previous state was {previous_state} ")

    return jsonify({'success': True})


@server.route('/stop_camera', methods=['POST'])
def stop_camera_handler():
    """
    Stops the camera function.

    Args:
        None.

    Returns:
        A JSON object containing a success status message.
    """
    return stop_camera()


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
    if os.path.exists(f'/home/{hostname}/Desktop/code/data/connected_devices.json'):
        with open(f'/home/{hostname}/Desktop/code/data/connected_devices.json', 'r') as f:
            connected_devices_data = json.load(f)
            print(connected_devices_data)
    return render_template('index.html', devices_data=connected_devices_data)

from flask import current_app


@server.route('/download_file', methods=['POST'])
def download():
    """
    Downloads a file from a remote device and saves it to the local file system.

    Args:
        None.

    Returns:
        None.
    """
    status.download()


@server.route('/start_server/<hostname>', methods=['POST'])
def start_server_from_home(hostname):
    start_server(hostname)


def send_request(url):
    response = requests.get(url)
    return response.text


@server.route('/download/<path:file_path>')
def serve_file(file_path):
    """
    Serves a file from the local file system.

    Args:
        file_path (str): The path to the file to serve.

    Returns:
        The requested file as an attachment.
    """

    create_json_data_file()
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)


@server.route('/data')
def data():
    """
    Reads data from a JSON file and renders it on a web page.

    Args:
        None.

    Returns:
        A rendered HTML template containing the data from the JSON file.
    """

    # read the JSON file
    with open(f'/home/{hostname}/Desktop/code/data/data.json') as f:
        information = json.load(f)

    # render the data template with the data
    return render_template('data.html', data=information)


@server.route('/status/<hostname>', methods=['GET'])
def server_status(user):
    """
    Retrieves the status of a specified server.

    Args:
        user (str): The name of the server to retrieve the status of.

    Returns:
        A rendered HTML template containing the status information of the specified server.
    """

    response = send_request('http://' + user + '.local:5000/')
    return render_template('start_server.html', response=response)


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


@server.route('/update_bandwidth', methods=['POST', 'GET'])
def update_bandwidth():
    """
    Updates the available bandwidth on the server.

    Args:
        None.

    Returns:
        A JSON object containing a success status message.
    """

    data_rate = request.get_json()
    new_value = data_rate['new_value']
    status.bandwidth = new_value
    print(f"Updated value: {status.bandwidth}")
    return jsonify({'success': True})


# Start the server on all network interfaces
if __name__ == '__main__':
    status.create_json_data_file()
    server.run(debug=True, host='0.0.0.0')
