import tflite_runtime.interpreter as tflite
import pandas as pd
import numpy as np
import time

#-----------------------------------------------------------------------------------------#

# Load the TensorFlow Lite model
interpreter = tflite.Interpreter(model_path='my_model.tflite')
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#------------------------------------------------------------------------------------------#

# Load data from a single CSV file
file_path = r"/home/pihand/Documents/KHKT_2024/data/a/a.0b1e01a7a75d.csv"  # Update with your file path

df = pd.read_csv(file_path)

# Process the data and extract features
# Assuming your first column is the timestamp and the remaining columns are the features
timestamps = df.iloc[:, 0]
features = df.iloc[:, 1:]  # Adjust the column index as per your data structure

# Add the features and label to the lists
x = features.values.flatten()
#print(x)

# Read the label_list from the text file
with open('label_list.txt', 'r') as f:
    label_list = [label.strip() for label in f.readlines()]

num_classes = len(label_list)

# Convert the lists into numpy arrays
x = np.array(x)

print(x.shape)

#------------------------------------------------------------------------------------------#


# Perform live testing
#while True:
# Capture and process input data
# ...

# Run inference
input_data = np.expand_dims(x.astype(np.float32), axis=0) # Provide input data as a NumPy array

interpreter.set_tensor(input_details[0]['index'], input_data)

start_time = time.time()*1000  # Start measuring time
print("Start time: ",time.time())
interpreter.invoke()
end_time = time.time()*1000  # End measuring time
print("Finish time: ",time.time())
output_data = interpreter.get_tensor(output_details[0]['index'])

# Process the output data
# ...
# Assuming output_data is a probability distribution over classes
predicted_class_index = np.argmax(output_data)
predicted_label_name = label_list[predicted_class_index]

print("Predicted Label: ", predicted_label_name)
print("Inference Time: ", end_time - start_time, "miliseconds")

# Display or use the processed output
# ...

