import socket

# Server configuration
HOST = '10.42.0.200'  # Server IP address
PORT = 8080  # Server port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Send data
    message = "Hello, client1!"
    sock.sendto(message.encode(), (HOST, PORT))

# Close the socket
sock.close()