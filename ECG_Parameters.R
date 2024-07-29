suppressMessages(library('nonlinearTseries'))

#list of disorders
disorders <- c("Bundle branch block",
              "Cardiomyopathy", 
              "Dysrhythmia",
              "Healthy control",
              "Myocardial infarction")

save_parameters <- function(disorder) {
  #This function saves the dimension and time lag values of ECG time series

  # CSV file saving path
  csv.path <- paste0("C:/Users/suraj/Desktop/PTB_data/patient_data_csv@250Hz/",disorder,"_parameters.csv")
  
  #Time series directory
  ecg_dir <- paste0("C:/Users/suraj/Desktop/PTB_data/patient_data_csv@250Hz/",disorder)
  ecg_files <- list.files(ecg_dir, pattern = ".csv", full.names = TRUE)

  results_df <- data.frame()
  for (file_path in ecg_files) {
    mdata <- read.csv(file_path, header = TRUE)
    col_names <- colnames(mdata)
    for (col_name in col_names) {
      column_name <- paste0(col_name)
      time_series <- mdata[[column_name]]
      emb_dim <- 0
      tau <- NULL
      tryCatch(
        {
          # time-lag calculation using autocorrelation function
          tau.acf <- timeLag(time_series, technique = "acf", selection.method = "first.minimum", lag.max = NULL, do.plot = F)
          # Embedding dimension calculation
          emb_dim <- estimateEmbeddingDim(time_series, time.lag = tau.acf, max.embedding.dim = 30 )
        
          subject_name <- basename(file_path)
          results_df <- rbind(results_df, c(subject_name, col_name, emb_dim, tau.acf))
        
          cat("Done\n")
        },
        error = function(e) {
          subject_name <- basename(file_path)
          results_df <- rbind(results_df, c(subject_name, col_name, 0, NA))
          cat("Error:", conditionMessage(e), "\n")
        }
      )
    }
  }

  colnames(results_df) <- c("subject", "ROI", "DIM", "TAU")
  # Results data frame to csv file
  write.csv(results_df, file = csv.path, row.names = FALSE)
}


# function calling
for (disease in diseases) {
  save_parameters(disease)
}

