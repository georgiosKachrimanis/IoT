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


@server.route('/connected')
def http_devices():
    return http_devices()


@server.route('/start_camera', methods=['POST'])
def start_camera_handler():
    return start_camera()


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
        data = json.load(f)

    # render the data template with the data
    return render_template('data.html', data=data)


@server.route('/status/<hostname>', methods=['GET'])
def server_status(hostname):
    response = send_request('http://' + hostname + '.local:5000/')
    return render_template('start_server.html', response=response)


@server.route('/end', methods=['GET'])
def end():
    return shutdown()



# Start the server on all network interfaces
if __name__ == '__main__':
    status.create_json_data_file()
    server.run(debug=True, host='0.0.0.0')
