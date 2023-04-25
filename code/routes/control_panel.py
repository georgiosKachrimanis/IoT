# routes/control_panel.py

from .connected_devices import devices
from flask import render_template

def control_panel():
    filtered_hostnames = devices().split('<br>')[:-1]
    return render_template('index.html', filtered_hostnames=filtered_hostnames)
