# routes/control_panel.py
from flask import render_template
import subprocess


def control_panel():
    filtered_hostnames = http_devices().split('<br>')[:-1]
    return render_template('index.html', filtered_hostnames=filtered_hostnames)


def devices():

    # get the list of connected devices
    connected_devices = subprocess.check_output(['sudo', 'arp', '-a', '-i', 'wlan0']).decode().split('\n')

    # parse the list of devices to get the hostnames
    hostnames = [device.split()[0].split('.')[0] for device in connected_devices if len(device.split()) > 0]

    # filter hostnames starting with pixxx
    filtered_hostnames = [hostname for hostname in hostnames if hostname.startswith('pi')]

    # return the response to the client
    return filtered_hostnames


def http_devices():
    filtered_hostnames = devices()
    # create a response string with the hostnames of the connected devices
    response = "<h1>Connected Devices:</h1><br>"
    for hostname in filtered_hostnames:
        response += f"{hostname}<br>"

    # return the response to the client
    return response