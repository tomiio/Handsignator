from tensorflow import keras
import tensorflow as tf
from keras.optimizers import Adam
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from collections import OrderedDict


# Load DATA
print("Loading data ...")
folder_path = r"C:\Users\Tom\Downloads\data" 
#folder_path = r"C:\Users\Tom\Downloads\KHKT_2024\python_collect_data\data"
folder_path = r"C:\Users\Tom\Downloads\data_new"

x = []
y = []
pre_rowleft = []
pre_rowright = []

def check_file_csv(arr):

    if all(arr[0:99][1:36]) == 0:
        for row in arr:
            if all(row[38:73]) == 0.0:
                return False
        return True

    if all(arr[0:99][38:73]) == 0:
        for row in arr:
            if all(row[1:36]) == 0.0:
                return False
        return True

    for row in arr:
        if all(row[1:36]) == 0.0:
            return False
        
        if all(row[38:73]) == 0.0:
            return False



for root, dirs, files in os.walk(folder_path):
    files.sort()
    for file_name in files:
        if file_name.endswith(".csv"):
            file_path = os.path.join(root, file_name)
            label = file_name.split(".")[0]  # Extract the label from the file name

            df = pd.read_csv(file_path)

            # Process the data and extract features
            # Assuming your first column is the timestamp and the remaining columns are the features
            timestamps = df.iloc[:, 0]
            features = df.iloc[:, 1:]  # Adjust the column index as per your data structure
            feature_array = features.values.flatten()

            data_check = features.values
            #print(data_check)

            #print(check_file_csv(data_check))
            
            # x.append(features.values.flatten())
            # y.append(label)
            if feature_array.dtype == np.float64 and feature_array.shape == (7400,):
                # Add the features and label to the lists
                x.append(features.values.flatten())
                y.append(label)
            else:
                print("Error: Files have invalid features: ",file_path)
                os.remove(file_path)

print("Done loading! converting data ...")

label_list = list(set(y))
label_list = list(OrderedDict.fromkeys(y))
num_classes = len(label_list)
print(label_list)
# Convert the lists into numpy arrays

# print(x)

x = np.array(x)
y = np.array(y)

# Perform label encoding
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("Split the data into training and testing sets")

# Split the data into training and testing sets
test_size = 0.2  # Percentage of data to use for testing (adjust as needed)
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=test_size, random_state=42)

x_train = keras.utils.normalize(x_train, axis=1)
x_test = keras.utils.normalize(x_test, axis=1)

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# x_train, x_val, y_train, y_val = train_test_split

# print(x_train[0].shape)
input_shape = x_train[0].shape

### TRAIN MODEL

print("Building model ...")

model = keras.Sequential([
    keras.layers.Dense(74, activation='relu', input_shape=input_shape),
    keras.layers.Dense(36, activation='relu'),
    keras.layers.Dense(18, activation='relu'),
    keras.layers.Dense(9, activation='relu'),
    keras.layers.Dense(6, activation='relu'),
    keras.layers.Dense(3, activation='relu'),
    keras.layers.Dense(num_classes, activation='softmax')  # Change activation to softmax
])

# Compile the model
learning_rate = 0.0005  # Set your desired learning rate
optimizer = Adam(learning_rate=learning_rate)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='logs')

print("Training model ...")

# Train the model
model.fit(x_train, 
          y_train, 
          validation_data = (x_train, y_train),
          epochs=100,
          callbacks = [tensorboard_callback])


# Evaluate model on test set
score = model.evaluate(x_test, y_test, verbose=0)
print(f"Test loss: {score[0]}")
print(f"Test accuracy: {score[1]}")


# Save the Keras model (If it's ok)
model.save('my_model.h5')

# Convert the Keras model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('my_model.tflite', 'wb') as f:
    f.write(tflite_model)


# Convert model to float16
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

tflite_fp16_model = converter.convert()
# Save the TensorFlow Lite float16 model
with open('my_model.tflite', 'wb') as f:
    f.write(tflite_model)

# Save the label_list as a text file if it doesn't exist
# if not os.path.exists('label_list.txt'):
with open('label_list.txt', 'w') as f:
    for label in label_list:
        f.write(label + '\n')

print(label_list)

