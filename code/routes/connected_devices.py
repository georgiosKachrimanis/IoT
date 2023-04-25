import subprocess


def devices():

    # get the list of connected devices
    devices = subprocess.check_output(['sudo', 'arp', '-a', '-i', 'wlan0']).decode().split('\n')

    # parse the list of devices to get the hostnames
    hostnames = [device.split()[0].split('.')[0] for device in devices if len(device.split()) > 0]

    # filter hostnames starting with pixxx
    filtered_hostnames = [hostname for hostname in hostnames if hostname.startswith('pi')]

    # create a response string with the hostnames of the connected devices
    response = "<h1>Connected Devices:</h1><br>"
    for hostname in filtered_hostnames:
        response += f"{hostname}<br>"

    # return the response to the client
    return response
