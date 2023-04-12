import subprocess
import os

# Path to your bash script file
bash_script_file = "ap.sh"

# Get the username of the current user
username = os.getlogin()

# Set the SSID to the username
ssid = username

# Define the password
password = "helloErgasia"

# Make sure the bash script is executable
subprocess.run(["chmod", "+x", bash_script_file])

# Run the bash script with the SSID and password as arguments
result = subprocess.run(["./" + bash_script_file, ssid, password], capture_output=True, text=True)

# Print the output of the bash script
print(result.stdout)

# Print the output of the bash script
print(result.stdout)

# Check if the script executed successfully
if result.returncode == 0:
    print("The bash script executed successfully.")
else:
    print("The bash script encountered an error.")
