import socket
#import time
import RPi.GPIO as GPIO
import multiprocessing

import tflite_runtime.interpreter as tflite
import pandas as pd
import numpy as np
import time
import os


BUTTON1_PIN = 5		# Classification mode
BUTTON2_PIN = 6		# Data collection mode
BUTTON3_PIN = 7		# Update model mode
		
	
# Bind the socket to a specific IP address and port
server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address1 = ('10.42.0.1', 2000)  # Use any available IP address and port number
server_socket1.bind(server_address1)

server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address2 = ('10.42.0.1', 3000)  # Use any available IP address and port number
server_socket2.bind(server_address2)

server_socket1.settimeout(0.02)
server_socket2.settimeout(0.02)	

print("Server is listening for incoming UDP packets...")

data1 = b"0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
data2 = b"1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
		
def process1(server_socket1,queue):
	buffer_to1 = 0
	while True:
		try:
			# Perform some computations or data processing
			data1, client_address1 = server_socket1.recvfrom(1024)
			
			server_socket1.settimeout(0.02)
			
			if buffer_to1 < 50:
				buffer_to1 += 1
			
			if buffer_to1 >= 50:
				server_socket1.settimeout(0.03)
			# Use the result as needed
		except socket.timeout:
			data1 = b"0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
			
			server_socket1.settimeout(0.02)

			if buffer_to1 > -50:
				buffer_to1 -= 1
							
			if buffer_to1 <= -50:
				server_socket1.settimeout(0.01)
				
		
		queue.put(data1)
		
		while queue.qsize() > MAX_QUEUE_SIZE:
			queue.get()

   
def process2(server_socket2,queue):
	buffer_to2 = 0
	while True:
		try:
			# Perform some computations or data processing
			data2, client_address2 = server_socket2.recvfrom(1024)
			
			server_socket1.settimeout(0.02)
			
			if buffer_to2 < 50:
				buffer_to2 += 1
			
			if buffer_to2 >= 50:
				server_socket2.settimeout(0.03)
			# Use the result as needed
		except socket.timeout:
			data2 = b"1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
			
			server_socket2.settimeout(0.02)

			if buffer_to2 > -50:
				buffer_to2 -= 1
							
			if buffer_to2 <= -50:
				server_socket2.settimeout(0.01)
			
		queue.put(data2)
		
		while queue.qsize() > MAX_QUEUE_SIZE:
			queue.get()
			
def process_collect_data(msg_queue,shared_button_state,shared_time_start):
	import time
	# Raspberry Pi GPIO pin for the button
	BUTTON_PIN = 17

	# Configure GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

	# Create a new UDP socket
	HOST = '10.42.0.1'  # Server IP address
	PORT = 8080  # Server port
	sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock1.bind((HOST,PORT))
	sock1.listen(1)
	client_sock, client_addr = sock1.accept()
	print("connected to: ", client_addr)

	i = 0
	shared_time_start.value = int(round(time.time()*1000))
	shared_button_state.value = False
	message_send = ""

	
	def button_callback(channel,shared_button_state,shared_time_start):
		# with shared_button_state.get_lock():
			# button_state = shared_button_state.value
		# with shared_time_start.get_lock():
			# time_start = shared_time_start.value
			
		#global start_time
		shared_time_start.value = int(round(time.time()*1000)) # Get the current time in milliseconds
		#global button_state
		shared_button_state.value = True
		title = "timestamp,left,a0x_0,a0y_0,a0z_0,g0x_0,g0y_0,g0z_0,a1x_0,a1y_0,a1z_0,g1x_0,g1y_0,g1z_0,a2x_0,a2y_0,a2z_0,g2x_0,g2y_0,g2z_0,a3x_0,a3y_0,a3z_0,g3x_0,g3y_0,g3z_0,a4x_0,a4y_0,a4z_0,g4x_0,g4y_0,g4z_0,a5x_0,a5y_0,a5z_0,g5x_0,g5y_0,g5z_0,right,a0x_1,a0y_1,a0z_1,g0x_1,g0y_1,g0z_1,a1x_1,a1y_1,a1z_1,g1x_1,g1y_1,g1z_1,a2x_1,a2y_1,a2z_1,g2x_1,g2y_1,g2z_1,a3x_1,a3y_1,a3z_1,g3x_1,g3y_1,g3z_1,a4x_1,a4y_1,a4z_1,g4x_1,g4y_1,g4z_1,a5x_1,a5y_1,a5z_1,g5x_1,g5y_1,g5z_1\n"
		print(title)
		client_sock.sendall(title.encode())
		
	
	# Add event listener to the button GPIO pin
	GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback = lambda channel:button_callback(channel,shared_button_state,shared_time_start), bouncetime = 500)

	while True:
		message = msg_queue.get()	
	
		#--------------------------------------------------------------#
		# SEND COLLECTING DATA TO PC CLIENT
		
		if shared_button_state.value == True:
			time_index = str(int(round(time.time()*1000)) - shared_time_start.value) # Get the time index in milliseconds
			
			message_send = time_index + "," + message +"\n"
			#print(len(message_send))
			try:
				client_sock.sendall(message_send.encode())
				print(message_send)
				i = i + 1
				if i >= 100:
					i = 0
					shared_button_state.value = False
					client_sock.sendall("E".encode())				
		
			except:
				print("client disconnected")
				sock1.close()
				client_sock.close()
				sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock1.bind((HOST,PORT))
				sock1.listen(1)
				client_sock, client_addr = sock1.accept()
				print("connected to: ", client_addr)
				shared_button_state.value = False
		#--------------------------------------------------------------#
		
				
	sock1.close()
	client_sock.close()
		
def classify_process(data3_queue):
	import tflite_runtime.interpreter as tflite
	import pandas as pd
	import numpy as np
		
	with open('label_list.txt', 'r') as f:
		label_list = [label.strip() for label in f.readlines()]

	num_classes = len(label_list)
		
		
	# Load the TensorFlow Lite model
	interpreter = tflite.Interpreter(model_path='my_model.tflite')
	interpreter.allocate_tensors()

	# Get input and output details
	input_details = interpreter.get_input_details()
	output_details = interpreter.get_output_details()
	
	while True:
		x = data3_queue.get()

		# Run inference
		input_data = np.expand_dims(x.astype(np.float32), axis=0) # Provide input data as a NumPy array
		interpreter.set_tensor(input_details[0]['index'], input_data)

		interpreter.invoke()

		output_data = interpreter.get_tensor(output_details[0]['index'])

		# Assuming output_data is a probability distribution over classes
		predicted_class_index = np.argmax(output_data)
		predicted_label_name = label_list[predicted_class_index]

		j = 0;
		for i in output_data[0]:
			print(f"Labe: {label_list[j]:<20}, {i:.4f}")
			j += 1
		print("Predicted Label: ", predicted_label_name)
		# print("Inference Time: ", end_time - start_time, "miliseconds")	
	
	
	
	
# Create shared variable between process
shared_button_state = multiprocessing.Value('b',False)
shared_time_start = multiprocessing.Value('d',0.0)
	
MAX_QUEUE_SIZE = 20  # Maximum size of the data queue
# Create a queue for inter-process communication
data1_queue = multiprocessing.Queue()
data2_queue = multiprocessing.Queue()
msg_queue = multiprocessing.Queue()
data3_queue = multiprocessing.Queue()

# Create two processes for receiving data
process1 = multiprocessing.Process(target=process1, args=(server_socket1, data1_queue))	# Left hand
process2 = multiprocessing.Process(target=process2, args=(server_socket2, data2_queue))	# Right hand
process3 = multiprocessing.Process(target=process_collect_data,  args = (msg_queue,shared_button_state,shared_time_start))	# Send to PC client
process4 = multiprocessing.Process(target=classify_process, args = (data3_queue,))
# Start the processes


# mode 1: classfication, process 1,2 and 3 activate
# mode 2: collecting data, 3 process have to be activated
# mode 3: update model, only process 4 activate

process1.start()	# LEFT HAND CLIENT
process2.start()	# RIGHT HAND CLIENT
process3.start()	# START COLLECTING DATA PROCESS

#process4.start()

# Receive and print data from the client
message_buffer = ""
data_buffer = []
# Read the label_list from the text file

while True:
	try:
		#--------------------------------------------------------------#
		# MODE 2
		# RECEIVING DATA FROM ESP32 CLIENT
		data1 = data1_queue.get()
		data2 = data2_queue.get()
			
		
		data1 = data1.decode('utf-8')
		data2 = data2.decode('utf-8')
		
		message = data1 + "," +  data2
		
		
		msg_queue.put(message)
		
		#print(message)
		#--------------------------------------------------------------#
		# MODE 1
		# SEND MESSAGE TO CLASSIFIER PROCESS
		
		# x = ...

		message_data = message.split(',')	
		data_buffer.append(message_data)
		
		if len(data_buffer) == 100:
			
			x = np.array(data_buffer)
			x = x.flatten()
			data3_queue.put(x)
			
			#print(x.shape)
			
				
			# # Load the TensorFlow Lite model
			# interpreter = tflite.Interpreter(model_path='my_model.tflite')
			# interpreter.allocate_tensors()

			# # Get input and output details
			# input_details = interpreter.get_input_details()
			# output_details = interpreter.get_output_details()
			
			# # Run inference
			# input_data = np.expand_dims(x.astype(np.float32), axis=0) # Provide input data as a NumPy array
			# interpreter.set_tensor(input_details[0]['index'], input_data)

			# start_time = time.time()*1000  # Start measuring time
			# #print("Start time: ",time.time())
			# interpreter.invoke()
			# end_time = time.time()*1000  # End measuring time
			# #print("Finish time: ",time.time())
			# output_data = interpreter.get_tensor(output_details[0]['index'])

			# # Assuming output_data is a probability distribution over classes
			# predicted_class_index = np.argmax(output_data)
			# predicted_label_name = label_list[predicted_class_index]

			# #print(output_data[0])
			# j = 0;
			# #os.system("clear")
			# for i in output_data[0]:
				# print(f"Labe: {label_list[j]:<20}, {i:.4f}")
				# j += 1
			# print("Predicted Label: ", predicted_label_name)
			# print("Inference Time: ", end_time - start_time, "miliseconds")

			# last line
			data_buffer = data_buffer[1:99][:]
		
		
		
		#--------------------------------------------------------------#
		# MODE 3
		# UPDATE MODE
		

		
	except KeyboardInterrupt:
		process1.terminate()
		process1.close()
		process2.terminate()
		process2.close()
		process3.terminate()
		process3.close()
		process4.terminate()
		process4.close()
		#process1.close()
		#process2.close()
		server_socket1.close()
		server_socket2.close()
		

# Close the socket
process1.close()
process2.close()
process3.close()
server_socket1.close()
server_socket2.close()
