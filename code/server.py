from flask import *
import psutil
import socket
import subprocess
from routes.connected_devices import devices
from routes.camera_control import start_camera, stop_camera
from routes.control_panel import control_panel
from routes.rpi_status import *
from routes.server_control import start_server


app = Flask(__name__)


@app.route('/connected')
def connected_devices():

    return devices()


@app.route('/start_camera', methods=['POST'])
def start_camera_handler():
    return start_camera()


@app.route('/stop_camera', methods=['POST'])
def stop_camera_handler():
    return stop_camera()


@app.route('/')
def home():
    # get the filtered hostnames from the devices function
    filtered_hostnames = devices().split('<br>')[:-1]

    # create an empty response string
    response = '<h1>Camera Control</h1>'

    # loop through the filtered hostnames and create a web page with the different functions for each device
    html_code = "<h2>Connected Devices:</h2><br>"
    for hostname in filtered_hostnames:
        if hostname.startswith('pi'):
            html_code += f"{hostname}:<br>"
            html_code += f"<form action='http://{hostname}.local:5000/start_camera' method='POST'>"
            html_code += "<input type='submit' value='Start Camera'>"
            html_code += "</form>"
            html_code += f"<form action='http://{hostname}.local:5000/stop_camera' method='POST'>"
            html_code += "<input type='submit' value='Stop Camera'>"
            html_code += "</form>"
            html_code += f"<form action='/start_server/{hostname}' method='POST'>"
            html_code += "<input type='submit' value='Start Server'>"
            html_code += "</form>"
            html_code += "<br>"

    # return the response to the client
    return html_code


@app.route('/index')
def index():
    return control_panel()


@app.route('/status', methods=['GET'])
def status():
    return device_status()


@app.route('/start_server/<hostname>', methods=['POST'])
def start_server_from_home(hostname):
    start_server(hostname)
    return "Server started successfully"


@app.route('/end', methods=['GET'])
def end():
    return shutdown()


# Start the server on all network interfaces
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
