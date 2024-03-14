import argparse
import os
import uuid
import socket
import csv

# Settings
DEFAULT_LABEL = "_unknown"  # Label prepended to all CSV files

def udp_in_waiting(sock):
    try:
        sock.setblocking(False)
        data = sock.recvfrom(1024)
        if data:
            return len(data[0])
        else:
            return 0
    except socket.error as e:
        if e.errno == socket.errno.EWOULDBLOCK:
            return 0
        else:
            raise

# Create a file with unique filename and write CSV data to it
def write_csv(data, dir, label):
    # Keep trying if the file exists
    exists = True
    while exists:
        # Generate unique ID for file (last 12 characters from uuid4 method)
        uid = str(uuid.uuid4())[-12:]
        filename = label + "." + uid + ".csv"
        # Create and write to file if it does not exist
        out_path = os.path.join(dir, filename)
        if not os.path.exists(out_path):
            exists = False
            try:
                with open(out_path, 'w') as file:
                    file.write(data)
                print("Data written to:", out_path)
            except IOError as e:
                print("ERROR:", e)
                return

# Command line arguments
parser = argparse.ArgumentParser(description="UDP Data Collection CSV")
# parser.add_argument('-p',
#                     '--port',
#                     dest='port',
#                     type=int,
#                     required=True,
#                     help="UDP port to listen on")
parser.add_argument('-d',
                    '--directory',
                    dest='directory',
                    type=str,
                    default=".",
                    help="Output directory for files (default = .)")
parser.add_argument('-l',
                    '--label',
                    dest='label',
                    type=str,
                    default=DEFAULT_LABEL,
                    help="Label for files (default = " + DEFAULT_LABEL + ")")

# Parse arguments
args = parser.parse_args()
# port = args.port
out_dir = args.directory
label = args.label

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the server address and port
server_address = ('10.42.0.1', 8080)  # Replace with the actual server IP address and port
sock.connect(server_address)

# print("UDP client is listening on port", port)
print("Output directory:", out_dir)
print("Label:", label)
print("Press 'ctrl+c' to exit")

# Make output directory
try:
    os.makedirs(out_dir)
except FileExistsError:
    pass

# Initialize variables for current set of data
current_data = []

# Loop forever (unless ctrl+c is captured)
try:
    while True:
        buffer = ""
        try:
            while True:
                try:
                    data, addr = sock.recvfrom(1024)    
                    print(1)
                    data = data.decode()
                    #if data[-5:] != "alive":
                        #print(data[len(data)
                    if data[len(data)-1] == "E": 
                        data = data[:len(data)-1]   
                        buffer += data
                        break
                    buffer += data
                    #data = data + "\n"
                except KeyboardInterrupt:
                    print(2)
                    print("Closing UDP socket")
                    sock.close()
                    break


            if buffer:
                print(buffer)
                buffer = buffer.strip()
                write_csv(buffer, out_dir, label)
                
        except KeyboardInterrupt:
            print("Closing UDP socket")
            sock.close()
            break

# Look for keyboard interrupt (ctrl+c)
except KeyboardInterrupt:
    print("Closing UDP socket")
    sock.close()
    

# Close the UDP socket
print("Closing UDP socket")
sock.close()