import streamlit as st
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow import keras


with st.sidebar: 
    # image = Image.open("C:/Users/TRUNG QUAN/Downloads/KHKT 2024/CODE/code app/Streamlit/hand.png")
    # st.image(image)
    st.title("Thiết bị chuyển ngữ hỗ trợ người câm điếc trong giao tiếp")
    choice = st.radio("Tùy chọn", ["Cập nhật dữ liệu", "Lập hồ sơ dữ liệu", "Huấn luyện mô hình", "Tải xuống"])
    st.info("Dự án tham gia cuộc thi Khoa học kỹ thuật cấp Tỉnh 2023-2024.")

# Load DATA
st.write("Loading data ...")
folder_path = r"C:\Users\Tom\Downloads\KHKT_2024\app\data"

"""

x = []
y = []

for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith(".csv"):
            file_path = os.path.join(root, file_name)
            label = file_name.split(".")[0]  # Extract the label from the file name

            df = pd.read_csv(file_path)

            # Process the data and extract features
            # Assuming your first column is the timestamp and the remaining columns are the features
            timestamps = df.iloc[:, 0]
            features = df.iloc[:, 1:]  # Adjust the column index as per your data structure

            # Add the features and label to the lists
            x.append(features.values.flatten())
            y.append(label)

label_list = list(set(y))
num_classes = len(label_list)

# Convert the lists into numpy arrays
x = np.array(x)
y = np.array(y)

# Perform label encoding
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data into training and testing sets
test_size = 0.2  # Percentage of data to use for testing (adjust as needed)
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=test_size, random_state=42)

x_train = keras.utils.normalize(x_train, axis=1)
x_test = keras.utils.normalize(x_test, axis=1)

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Build the model
model = keras.Sequential([
    keras.layers.Dense(20, activation='relu', input_shape=(1800,)),
    keras.layers.Dense(20, activation='relu'),
    keras.layers.Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=30, verbose=0)

# Evaluate the model on the test set
score = model.evaluate(x_test, y_test, verbose=0)

# Display the results
st.write(f"Test loss: {score[0]}")
st.write(f"Test accuracy: {score[1]}")

"""