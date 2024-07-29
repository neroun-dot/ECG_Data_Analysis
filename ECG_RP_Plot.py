#importing necessary libraries
import os
import gc
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

# List of Cardiac Disorders
disorders = ["Bundle branch block",
             "Cardiomyopathy",
             "Dysrhythmia",
             "Healthy control",
             "Myocardial infarction"]



def recurrence_plot(df, name=None, tau=1, dim=1):
    '''This function generates a recurrence plot using a 1-dimensional column vector. 
    The pdist function computes the Euclidean distances between states, 
    while the squareform function creates a symmetric data matrix from these distances.

    Input: 1-dimensional column vector
    Output: PNG image

    The patterns and inferences from the image are dependent on the values of tau and dim.

    dim: Optimal embedding dimension (determined using Cao's method or the false nearest neighbors algorithm)
    tau: Time lag (determined by the first minimum of the autocorrelation function)
    
    To obtain a 224 x 224 image with a figsize of (4, 4), set dpi to 56 (since 224/4 = 56).'''

    df = df.reshape(-1, 1) # 1D column vector
    tuple_vector = [[df[i + j * tau][0] for j in range(dim)] for i in range(len(df) - dim * tau)]
    states = pdist(tuple_vector) # euclidean distance 
    m_states = squareform(states)

    fig = plt.figure(frameon=False)
    fig.set_size_inches(4, 4)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(m_states, aspect="auto", cmap="gray")
    plt.savefig(name + ".png", dpi=56, bbox_inches="tight")
    plt.close()
    gc.collect()

def get_plot(disorder):
    '''This function collects the ecg singal,dim and tau of a specific channel and
       fed it into recurrence_plot function to get recurrence plots. 
       
       input : path to ecg signal; and dim, and tau values
       output : signal, dim, and tau for creating recurrence plots'''

    # dirctory to ECG data files
    data_dir = f"/path to Ecg signal csv files/{disorder}"
    os.chdir(data_dir)

    # CSV file containing dim and tau values of specific channels
    df = pd.read_csv(f"/path to dim and tau values/{disorder}_parameters.csv")
    ecg_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

    excluded_list = []

    for file in ecg_files:
        ecg_data = pd.read_csv(os.path.join(data_dir, file))
    
    for column in ecg_data.columns:
        for sub_name in df['subject'].unique():
            subject_data = df[(df["subject"] == sub_name) & (df["ROI"] == column)]
            if subject_data.empty:
                continue
            
            # extracting dim and tau for specific channel
            dim = int(subject_data['DIM'].iloc[0])
            tau = int(subject_data['TAU'].iloc[0])
            time_data = ecg_data[[column]].values

            plot_filename = f"{data_dir}/{sub_name[0:8]}_roi_{column}.png"
            if tau * dim < 1000:
                if os.path.exists(plot_filename):
                    continue
                # generating the recurrence plot
                recurrence_plot(time_data, name=f"{data_dir}/{sub_name[0:8]}_roi_{column}", tau=tau, dim=dim)
            else:
                excluded_list.append((sub_name, column, dim, tau))

    gc.collect()

#function calling
for disorder in disorders:
	get_plot(disorder)
