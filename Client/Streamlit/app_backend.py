import streamlit as st
from PIL import Image
from tensorflow import keras
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import subprocess

with st.sidebar: 
    image = Image.open(r"C:\Users\Tom\Downloads\KHKT_2024\Streamlit\hand.png")
    st.image(image)
    st.title("Thiết bị chuyển ngữ hỗ trợ người câm điếc trong giao tiếp")
    choice = st.radio("Tùy chọn", ["Giới thiệu","Lấy dữ liệu","Huấn luyện mô hình"])

def run_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return output.decode()


if choice == "Giới thiệu":
    st.info("Dự án tham gia cuộc thi Khoa học kỹ thuật cấp Tỉnh 2023-2024.")


if choice == "Lấy dữ liệu":
    st.title("Lấy dữ liệu")
    sign = st.text_input("Đặt tên cho cử chỉ:")
    if sign:
        command =  "python udp-data-collect.py -d " + sign + " -l " + sign 
        #command = "python test"+sign+".py"
        st.write(command)

        if command:
            output = run_command(command)
            st.code(output)


    


if choice == "Huấn luyện mô hình":
    st.title("Huấn luyện mô hình")


    folder_path = st.text_input("Hãy nhập đường dẫn đến thư mục")
    if folder_path:
        st.success("Chọn thư mục thành công!")
        st.write("Đang tải lên dữ liệu của bạn...")

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

        # print(x_train[0].shape)
        input_shape = x_train[0].shape

        st.success("Đã tải dữ liệu thành công! Đang chuyển sang bước Huấn luyện mô hình.")
        ### TRAIN MODEL


        st.write("Đang huấn luyện mô hình máy học...")

        model = keras.Sequential([
            keras.layers.Dense(30, activation='relu', input_shape=input_shape),
            keras.layers.Dense(30, activation='relu'),
            keras.layers.Dense(num_classes, activation='softmax')  # Change activation to softmax
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


        print("Training model ...")

        # Train the model
        epochs = 30
        losses = []
        accuracies = []
        for epoch in range(epochs):
            # Perform model training for each epoch
            history = model.fit(x_train, y_train)
            
            # Display the epoch information in Streamlit
            losses.append(history.history['loss'][0])
            accuracies.append(history.history['accuracy'][0])

            st.write(f"Epoch {epoch+1}/{epochs} hoàn thành:")
            st.write(f"Sai số: {losses[-1]}, Độ chính xác: {accuracies[-1]}")
            st.write()

        # Evaluate model on test set
        score = model.evaluate(x_test, y_test, verbose=0)

        st.success("Mô hình đã được huấn luyện thành công!")
        st.write(f"Sai số: {score[0]}")
        st.write(f"Độ chính xác: {score[1]}")

