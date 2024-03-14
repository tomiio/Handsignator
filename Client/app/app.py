import streamlit as st
import pandas as pd
import os
from PIL import Image

import ydata_profiling
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from pycaret.regression import setup, compare_models, pull, save_model



with st.sidebar: 
    image = Image.open("C:/Users/TRUNG QUAN/Downloads/KHKT 2024/CODE/code app/Streamlit/hand.png")
    st.image(image)
    st.title("Thiết bị chuyển ngữ hỗ trợ người câm điếc trong giao tiếp")
    choice = st.radio("Tùy chọn", ["Cập nhật dữ liệu", "Lập hồ sơ dữ liệu", "Huấn luyện mô hình", "Tải xuống"])
    st.info("Dự án tham gia cuộc thi Khoa học kỹ thuật cấp Tỉnh 2023-2024.")

if os.path.exists("sourcedata.csv"):
    df = pd.read_csv("sourcedata.csv", index_col=None)

if choice == "Cập nhật dữ liệu":
    st.title("Tải lên")
    file = st.file_uploader("Cập nhật dữ liệu của bạn")
    if file: 
        df = pd.read_csv(file, index_col=None)
        df.to_csv('sourcedata.csv', index=None)
        st.dataframe(df)
    # if st.button("Start Training"):
    #     pass

if choice == "Lập hồ sơ dữ liệu":
    st.title("Phân tích dữ liệu")
    profile = ProfileReport(df)
    st_profile_report(profile)

if choice == "Huấn luyện mô hình":
    st.title("Huấn luyện mô hình")
    target = st.selectbox("Chọn mục tiêu",df.columns)
    setup(df, target=target, silent=True)
# If you've installed the PyCaret master branch or a 3.0 release candidate, you will find that the silent argument was
# removed 11 days ago. The documentation you're looking at is for a stable release, 2.3, which has the silent argument.
    setup_df = pull()
    st.info("Thông số mô hình học máy")
    st.dataframe(setup_df)
    best_model = compare_models()
    compare_df = pull()
    st.info("Mô hình đã được huấn luyện")
    st.dataframe(compare_df)
    best_model
    
