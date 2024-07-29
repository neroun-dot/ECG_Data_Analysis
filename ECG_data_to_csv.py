#importing necessary libaries
import os
import wfdb # waveform database
import pandas as pd

# list of Diseases
diseases=["Bundle branch block","Heart failure","Cardiomyopathy","Dysrhythmia","Healthy control","Miscellaneous","Myocardial infarction","Myocarditis","Valvular heart disease",""]

def save_data(disease):
    '''This function takes the ECG data in form of subject.dat and subject.hea files. 
       Subject.dat file contains the ECG signal of paitent and Subject.hea file contains 
       paitent's medical informtion. for a particular disease the function read the .hea 
       files and retrive the information from corresponding .dat file.  '''
    
    # Creating directory to store the disease specific files
    directory = f"C:/Users/suraj/Desktop/PTB_data/Patient_data_csv@250Hz/{disease}"
    os.makedirs(directory, exist_ok=True)

    # Directory to all files
    parent_directory ="C:/Users/suraj/Desktop/PTB_data/patient_data" 
    contents = os.listdir(parent_directory)
    
    # Paths to all the folders in the parent directory
    folder_paths = [os.path.join(parent_directory, item) for item in contents if os.path.isdir(os.path.join(parent_directory, item))]
    for folder_path in folder_paths:
        os.chdir(folder_path)
        hea_files = [f for f in os.listdir() if f.endswith('.hea')]

        for file in hea_files:
            with open(file, 'r') as hea_file:
                hea_content = hea_file.read()
                # checking if the disease is mentioned in the .hea file
                if  f'{disease}' in hea_content:
                    file_name = file.split('.')[0]
    
                    record = wfdb.rdrecord(file_name)
                    signal_names = record.sig_name # read the ECG Channels
                    signal_values = record.p_signal # read the values of specific Channels

                    # downsample the orginal data from 1000Hz to 250Hz
                    df_data = {signal_name: signal_values[::4, index] for index, signal_name in enumerate(signal_names)}
    
                    df = pd.DataFrame(df_data)
                    (df.to_csv(os.path.join(directory, file_name + '.csv'), index=False))

# function calling
for disease in diseases:
    save_data(disease)
            