import socket

# Client configuration
HOST = '10.42.0.1'  # Server IP address
PORT = 8080  # Server port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the client IP and port
sock.connect((HOST, PORT))
try:      
    while True:
        # Receive data
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        print("Received:", message)
except KeyboardInterrupt:
	sock.close()
# Close the socket
sock.close()