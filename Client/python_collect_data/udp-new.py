
import socket
HOST = "10.42.0.1"
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

try:
    while True:
        try:
            data, address = sock.recvfrom(1024)
            data = data.decode()
            print(data[-5:])
            if data[len(data) - 6 : len(data) - 1] == "alive":
                pass
            else:
                pass
                #print(data)
        except KeyboardInterrupt:
            sock.close()
        #print(data.decode())
except KeyboardInterrupt:
    sock.close()

