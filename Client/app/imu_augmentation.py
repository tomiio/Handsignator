import os
import pandas as pd
import numpy as np

# Define the path to the folder containing the CSV files
folder_path = r'C:\Users\Tom\Downloads\data_new\moojt'

# Define the augmentation parameters
augmentation_factor = 2  # Number of augmented samples to generate
noise_std = 0.01  # Standard deviation of the noise

# Define the column indices to exclude from augmentation
columns_to_exclude = [2,3,4,8,9,10,14,15,16,20,21,22,26,27,28,32,33,34,38,39,40,45,46,47,51,52,53,57,58,59,63,64,65,69,70,71] # Columns to exclude (zero-based index)
#[1,2,3,7,8,9,13,14,15,19,20,21,25,26,27,31,32,33,37,38,39,44,45,46,50,51,52,56,57,58,62,63,64,68,69,70]
#[2,3,4,8,9,10,14,15,16,20,21,22,26,27,28,32,33,34,38,39,40,45,46,47,51,52,53,57,58,59,63,64,65,69,70,71]
# Iterate over the CSV files in the subfolder
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.csv'):
            # Read the original CSV file
            file_path = os.path.join(root, file)
            original_data = pd.read_csv(file_path)

            # Apply noise augmentation
            augmented_data = original_data.copy()

 
            #for _ in range(augmentation_factor):
            noise = np.random.normal(-noise_std, noise_std)
            #print(len(noise))
            try:
                for i in columns_to_exclude:
                    augmented_data.iloc[:, i] = augmented_data.iloc[:, i].astype(float) + noise


                # Create a new file name for the augmented data
                new_file_name = os.path.splitext(file)[0] + '1.csv'
                new_file_path = os.path.join(root, new_file_name)

                # Save the augmented data to a new CSV file
                augmented_data.to_csv(new_file_path, index=False)

                print(f"Augmented data saved to: {new_file_path}")
            except:
                pass