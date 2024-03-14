import os
import pandas as pd
import numpy as np

folder_path = r"C:\Users\Tom\Downloads\data" 


def check_file_csv(arr):

    # 1 : 37 ---- 38 : 74
    check = True
    avg_arr = np.array([0.0]*74)
    cnt = 0
    for a in arr:
        if all(a[1:37] == 0) or all(a[38:74] == 0):
            avg_arr += a
            cnt += 1

    if cnt != 0:
        avg_arr = [round(num / cnt,2) for num in avg_arr]
        check = False
            
    print(check)
    print(arr[0:100,0:37])
    print(arr[0:100,38:74])

    result = []

    if check == False:
        for a in arr:
            # print
            if arr[0:100,0:37].all() == 0.0:
                if all(a[38:74] == 0.0):
                    result.append(avg_arr)
                    check = False
                else:
                    result.append(a)

            elif arr[0:100,38:74].all() == 0.0:
                if all(a[1:37] == 0.0):
                    result.append(avg_arr)
                    check = False
                else:
                    result.append(a)            
            
    result = np.array(result)
    return result, check


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
            print(feature_array.shape)
            if (feature_array.dtype == np.float64 and feature_array.shape == (7400,)):

                data_check = features.values
                #print(data_check)
                data_check, check = check_file_csv(data_check)
                #print(data_check) 
                # REWRITE TO ORIGINAL CSV FILE
                # Rewrite to the original CSV file
                if check == False:
                    df.iloc[:, 1:] = data_check
                    df.to_csv(file_path, index=False)
                    print("Rewrite file: ",file_path)

            else:
                #count = count + 1
                print(" Error: Files have invalid features: ",file_path)
                os.remove(file_path)
    count = 0