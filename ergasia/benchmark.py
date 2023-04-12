import os
import psutil
import time
import subprocess
import pandas as pd

# Set the test duration and number of CPU cores to use
duration = 30  # test duration in seconds
num_cores = psutil.cpu_count(logical=False)  # number of physical CPU cores

# Get the path to the desktop directory for the current user
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Set the output file path to the desktop directory
output_file = os.path.join(desktop_path, "cpu_usage.log")

# Open the output file for writing
with open(output_file, 'w') as f:
    # Run the stress test and record the CPU usage
    for i in range(duration):
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        f.write(','.join([str(percent) for percent in cpu_percent]) + '\n')
        time.sleep(1)

# Set the path to the cpu_usage.log file
log_file_path = os.path.join(desktop_path, "cpu_usage.log")

# Load the cpu_usage.log file into a DataFrame
df = pd.read_csv(log_file_path, header=None)

# Calculate the CPU usage statistics for each core
stats = df.describe()

# Print the CPU usage statistics
print(stats)

# Run the mount command and capture the output
output = subprocess.check_output(['mount'])

# Parse the output to extract the device path for the boot device
for line in output.decode().split('\n'):
    if ' /boot' in line:
        device_path = line.split()[0]
        break

# Run the hdparm read test and capture the output
storage = subprocess.check_output(['sudo', 'hdparm', '-t', output])

# Parse the output to extract the read performance metric
read_speed = float(storage.decode().split()[-2])

# Print the read performance metric
print(f"SSD read speed: {read_speed} MB/s")