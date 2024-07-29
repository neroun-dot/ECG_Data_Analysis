# Non-linear Analysis Based ECG Classification of Cardiac Disorders

## Steps to Execute the Code

1. **Data Acquisition**:
   - The ECG data is taken from the [Physionet database](https://physionet.org/). Each recording is provided as `.dat` and `.hea` files.
   - `.dat` file contains the time series, and `.hea` contains the patient's medical information.

2. **Convert ECG Data to CSV**:
   - Script: `ECG_data_to_csv.py`
   - This script takes the ECG data in `.dat` and `.hea` formats.
   - It reads the `.hea` files and retrieves the information from the corresponding `.dat` file, converting them into CSV files for a particular disease.

3. **Save ECG Parameters**:
   - Script: `ECG_Parameters.R`
   - This script saves the dimension and time lag values of the ECG time series.

4. **Plot Recurrence Plots**:
   - Script: `ECG_RP_Plot.py`
   - This script takes a specific channel's signal data, dimension (`dim`), and time lag (`tau`).
   - It converts the time series into 1D column vectors and, using the `dim` and `tau` values, creates a tuple vector.
   - The Euclidean distance between the elements of a tuple vector is used to plot the recurrence plots.

5. **Generate Latent Space Embeddings**:
   - Scripts: `embeddings-classifier.ipynb` and `rqa-classifier.ipynb`
   - These scripts take a 15 x 224 x 224 tensor input and reduce the dimension to 14 x 14 embeddings using an autoencoder.

6. **CNN Classifier for Cardiac Classification**:
   - Script: `embeddings-classifier.ipynb`
   - This script uses a CNN classifier for cardiac classification.
   - The input to the model is the latent space embeddings.

7. **Stacked Classifier for RQA Features**:
   - Script: `rqa-classifier.ipynb`
   - This script uses a stacked classifier consisting of SVM, XGBOOST, and RUSBOOST models.
   - The input to the model is the Recurrence Quantification Analysis (RQA) features of latent space embeddings.
