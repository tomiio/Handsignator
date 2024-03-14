import paramiko

# Define the file paths on your computer and Raspberry Pi

local_model_file = r'C:\Users\Tom\Downloads\KHKT_2024\app\my_model.tflite'
#local_model_file = r'C:\Users\Tom\Downloads\KHKT_2024\app\ei.tflite'
local_label_file = r'C:\Users\Tom\Downloads\KHKT_2024\app\label_list.txt'
remote_model_file = '/home/pihand/Documents/KHKT_2024/my_model.tflite'
remote_label_file = '/home/pihand/Documents/KHKT_2024/label_list.txt'


# Define the Raspberry Pi's IP address, username, and password
raspberry_pi_ip = '10.42.0.1'
username = 'pihand'
password = 'pihand'

# Create an SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the Raspberry Pi
    ssh_client.connect(raspberry_pi_ip, username=username, password=password)

    # Create an SFTP client over the SSH connection
    sftp_client = ssh_client.open_sftp()

    # Transfer the files
    sftp_client.put(local_model_file, remote_model_file)
    sftp_client.put(local_label_file, remote_label_file)

    print("Model on server are updated!")

    # Close the SFTP client
    sftp_client.close()

finally:
    # Close the SSH client
    ssh_client.close()