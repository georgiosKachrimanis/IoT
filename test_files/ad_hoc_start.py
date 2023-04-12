import os
import subprocess
# Set the path to the bash script
script_name = "ad_hoc.sh"
script_path = os.path.join(os.path.expanduser("~/Desktop"), script_name)

# Make the adhoc_config.sh script executable
os.chmod(script_path, 0o755)

# Run the adhoc_config.sh script
subprocess.run(["sudo", script_path])


