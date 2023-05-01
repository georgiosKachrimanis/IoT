
from flask import render_template
from .status import devices
import subprocess


def control_panel():
    filtered_hostnames = http_devices().split('<br>')[:-1]
    return render_template('index.html', filtered_hostnames=filtered_hostnames)


def http_devices():
    filtered_hostnames = devices()
    # create a response string with the hostnames of the connected devices
    response = "<h1>Connected Devices:</h1><br>"
    for hostname in filtered_hostnames:
        response += f"{hostname}<br>"

    # return the response to the client
    return response


