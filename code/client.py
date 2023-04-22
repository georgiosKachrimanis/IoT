import socket

def get_ap_ip():
    hostname = socket.gethostname()  # Get the local device's hostname
    ip_address = socket.gethostbyname(hostname)  # Get the local device's IP address
    return ip_address


server_ip = get_ap_ip()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, 12345))

while True:
    message = input("Enter your message ('exit' to quit): ")
    if message.lower() in ["exit", "quit"]:
        break
    client_socket.send(message.encode('utf-8'))

client_socket.close()
