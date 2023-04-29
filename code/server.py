from flask import *
from routes import status
from routes.camera_control import start_camera, stop_camera
from routes.control_panel import devices
from routes.control_panel import control_panel
from routes.server_control import start_server, check_server_status
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
    server_ips = devices()
    # get the server IP address and file path from the request form
    for i in server_ips:
        file_path = 'data/data.json'
        localhost = status.get_device_name()
        print(file_path)

        # construct the URL of the file on the remote server
        url = f'http://{i}@{i}.local:5000/download/{file_path}'
        print(url)
        # download the file and save it to the local file system
        file_name = file_path.split('/')[-1]
        local_file_path = f'/home/{localhost}/Desktop/code/data/{i}data.json' # Remove the 'pi' prefix from i
        download_file(url, local_file_path)
        print(url + "and this is the " + local_file_path)
    # return a response to the client
    return f'Downloaded file from '


@server.route('/index')
def index():
    return control_panel()


@server.route('/start_server/<hostname>', methods=['POST'])
def start_server_from_home(hostname):
    start_server(hostname)


def send_request(url):
    response = requests.get(url)
    return response.text


@server.route('/download/<path:file_path>')
def serve_file(file_path):
    print(f'////////{file_path}/////////////')
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


def download_file(url, file_path):

    response = requests.get(url, stream=True)
    print(f"**********FILE PATH:{file_path}")
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return file_path


# Start the server on all network interfaces
if __name__ == '__main__':
    status.create_json_data_file()
    server.run(debug=True, host='0.0.0.0')
