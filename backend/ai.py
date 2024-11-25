import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.metrics import mean_squared_error

# Step 1: Load and combine CSV files
file_paths = [
    './data/Realisasi Pendapatan Negara, 2007-2009.csv',
    './data/Realisasi Pendapatan Negara, 2010-2012.csv',
    './data/Realisasi Pendapatan Negara, 2013-2015.csv',
    './data/Realisasi Pendapatan Negara, 2016-2018.csv',
    './data/Realisasi Pendapatan Negara, 2019-2021.csv',
    './data/Realisasi Pendapatan Negara, 2022-2024.csv'
]

data_frames = [pd.read_csv(file) for file in file_paths]
data = pd.concat(data_frames, ignore_index=True)

# Transpose the DataFrame if the target data is in a row
data = data.T

# Step 2: Preprocess the data
# Convert all columns to numeric, forcing non-numeric values to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Fill missing values with mean
data.fillna(data.mean(), inplace=True)

# # Separate features and target variable
# X = data.drop('target_column', axis=1)  # Replace 'target_column' with your target column name
# y = data['target_column']

# Extract the target row
target_row_name = 'Penerimaan Perpajakan'  # Replace with the actual name of the target row
y = data.loc[target_row_name]

# Drop the target row from the features
X = data.drop(target_row_name)

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 4: Train a Gaussian Process Regression model
# Define the kernel
kernel = C(1.0, (1e-4, 1e1)) * RBF(1.0, (1e-4, 1e1))

# Create the Gaussian Process model
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=1e-2)

# Fit the model
gpr.fit(X_train, y_train)

# Step 5: Make predictions and evaluate the model
y_pred, sigma = gpr.predict(X_test, return_std=True)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Optional: Print the predicted values and their uncertainties
for i in range(len(y_pred)):
    print(f'Prediction: {y_pred[i]}, Uncertainty: {sigma[i]}')