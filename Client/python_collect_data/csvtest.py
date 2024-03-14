import argparse
import csv
import uuid
import os

data = "timestamp,0,a0x_0,a0y_0,a0z_0,g0x_0,g0y_0,g0z_0,a1x_0,a1y_0,a1z_0,g1x_0,g1y_0,g1z_0,a2x_0,a2y_0,a2z_0,g2x_0,g2y_0,g2z_0,a3x_0,a3y_0,a3z_0,g3x_0,g3y_0,g3z_0,a4x_0,a4y_0,a4z_0,g4x_0,g4y_0,g4z_0,a5x_0,a5y_0,a5z_0,g5x_0,g5y_0,g5z_0\n1,1,-1.97,2.90,-9.10,0.00,0.00,0.00,-6.49,-7.14,1.18,-6.49,-7.14,1.18,-6.18,3.95,5.79,-6.18,3.95,5.79,1.71,0.96,-9.64,1.71,0.96,-9.64,10.17,-0.57,-0.48,10.17,-0.57,-0.48,-4.99,2.95,7.83,-4.99,2.95,7.83\n7,1,-1.96,2.88,-9.12,0.00,0.00,0.00,-6.49,-7.14,1.17,-6.49,-7.14,1.17,-6.18,3.95,5.79,-6.18,3.95,5.79,1.71,0.96,-9.64,1.71,0.96,-9.64,10.17,-0.56,-0.47,10.17,-0.56,-0.47,-4.99,2.94,7.82,-4.99,2.94,7.82"

DEFAULT_LABEL = "_unknown"  # Label prepended to all CSV files

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
                    # writer = csv.writer(file)
                    # writer.writerows(data.split(','))

                    file.write(data)
                    # l = 0
                    # while l < len(data):
                    #     print(data[l].split(','))
                    #     data[l] = data[l].split(',')
                    #     writer.writerows(data[l])
                    #     l += 1
                print("Data written to:", out_path)
            except IOError as e:
                print("ERROR:", e)
                return

data = data.strip()
print(data)

write_csv(data, out_dir, label)