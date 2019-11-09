import socket
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "lib"))
import util  # noqa
import encrypted_msg   # noqa

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the remote host and port
sock.connect(('192.168.42.91', 6969))

# Create a personal key.
key = encrypted_msg.generate_key()

# Send a request to the host
encrypted_msg.send(sock, "Why don't you call me anymore?\r\n")

# Get the host's response, no more than, say, 1,024 bytes
response_data = encrypted_msg.recv(sock, key)

print(response_data)

# Terminate
sock.close()