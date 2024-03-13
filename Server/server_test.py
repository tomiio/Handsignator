import socket
import time

# Server configuration
HOST = '10.42.0.1'  # Server IP address
PORT = 8080  # Server port

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(1)
client_sock, client_addr = sock.accept()
print("connected to: ", client_addr)
message = "abcd"

try:
	while True:
		# Send data
		#message = "abcd"
		#sock.sendto(message.encode(),(HOST, PORT))
		try:
			client_sock.sendall(message.encode())
		except:
			sock.close()
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.bind((HOST,PORT))
			sock.listen(1)
			client_sock, client_addr = sock.accept()
			print("connected to: ", client_addr)
		time.sleep(3)
		message = "alive"
except KeyboardInterrupt:
	sock.close()
# Close the socket
sock.close()
