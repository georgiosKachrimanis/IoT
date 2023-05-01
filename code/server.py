from flask import *

import routes
from routes import status
from routes.camera_control import start_camera, stop_camera
from routes.server_control import start_server
from routes.status import *
import requests

server = Flask(__name__)
status.create_json_data_file()
hostname = status.get_device_name()
available = True
previous_state = 'nothing'
print(status.bandwidth)


@server.route('/camera', methods=['GET', 'POST'])
def camera():
    clients = devices()
    data =request.get_json()

    print(f"Received: {data}")
    if data['action'] == 'start':
        message = {'message': 'start_camera'}
    elif data['action'] == 'stop':
        message =  {'message': 'stop_camera'}
    else:
        message = {'message': 'this is a test'}

    for client in clients:
        url = f'http://{client}@{client}:5000/start_camera'
        requests.post(url, json=message)

    return jsonify({'success': True})

@server.route('/connected')
def http_devices():
    return http_devices()


@server.route('/start_camera', methods=['POST'])
def camera_handler():
    data = request.get_json()
    message = data['message']
    global previous_state
    if message == 'start_camera' and previous_state != message:
        # Start the camera function
        print(f"Starting camera... the previous state was {previous_state}")
        previous_state = message
    elif message == 'stop_camera' and previous_state != message:
        # Stop the camera function
        previous_state = message
        print(f"Stopping camera... the previous state was {previous_state}")
    else:
        print(f"Unknown message received and the previous state was {previous_state} ")

    return jsonify({'success': True})


@server.route('/stop_camera', methods=['POST'])
def stop_camera_handler():
    return stop_camera()


@server.route('/')
def home():
    return render_template('hello.html')


@server.route('/download_file', methods=['POST'])
def download():
    status.download()


@server.route('/index')
def index():
    return render_template('hello.html')


@server.route('/start_server/<hostname>', methods=['POST'])
def start_server_from_home(hostname):
    start_server(hostname)


def send_request(url):
    response = requests.get(url)
    return response.text


@server.route('/download/<path:file_path>')
def serve_file(file_path):
    create_json_data_file()
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e)


@server.route('/data')
def data():
    # read the JSON file
    with open(f'/home/{hostname}/Desktop/code/data/data.json') as f:
        information = json.load(f)

    # render the data template with the data
    return render_template('data.html', data=information)


@server.route('/status/<hostname>', methods=['GET'])
def server_status(hostname):
    response = send_request('http://' + hostname + '.local:5000/')
    return render_template('start_server.html', response=response)


@server.route('/end', methods=['GET'])
def end():
    return shutdown()


@server.route('/update_bandwidth', methods=['POST', 'GET'])
def update_bandwidth():
    print("What the fuck")
    datare = request.get_json()
    print(f"Received new value")
    new_value = datare['new_value']
    print(f"Received new value: {new_value}")
    print(f"Current value: {status.bandwidth}")
    status.bandwidth = new_value
    print(f"Updated value: {status.bandwidth}")
    return jsonify({'success': True})


# Start the server on all network interfaces

if __name__ == '__main__':
    status.create_json_data_file()
    server.run(debug=True, host='0.0.0.0')
