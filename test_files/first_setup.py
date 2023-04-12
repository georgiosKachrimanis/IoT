import os
import subprocess

# Set the path to the bash script
script_name = "init_setup.sh"
script_path = os.path.join(os.path.expanduser("~/Desktop"), script_name)

# Set the execute permission on the bash script
os.chmod(script_path, 0o755)

# Call the bash script with sudo privileges
subprocess.run(["sudo", script_path])


