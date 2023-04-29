import subprocess
import requests


def start_server(hostname):
    # password for SSH connection
    password = 'ergasia'

    # construct the ssh command to start the server
    ssh_command = f"sshpass -p {password} ssh {hostname}@{hostname}.local 'sudo python3 ~/Desktop/code/server.py'"

    # start the server on the remote device using ssh
    subprocess.run(ssh_command, shell=True)


def check_server_status(hostname):

    # construct the URL for the server's endpoint
    url = f"http://{hostname}.local:5000/"
    # send an HTTP POST request to the server's endpoint
    response = requests.post(url)
    return response



