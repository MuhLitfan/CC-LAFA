import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from sklearn.preprocessing import StandardScaler
import glob
import os
import matplotlib.pyplot as plt

class TimeSeriesGP:
    def __init__(self, length_scale=1.0, noise_level=1.0):
        """
        Initialize the Gaussian Process model for time series analysis.
        
        Parameters:
        length_scale (float): The length scale of the RBF kernel
        noise_level (float): The noise level for the WhiteKernel
        """
        # Define the kernel as sum of RBF and WhiteKernel for noise
        self.kernel = RBF(length_scale=length_scale) + WhiteKernel(noise_level=noise_level)
        
        # Initialize the Gaussian Process Regressor
        self.model = GaussianProcessRegressor(
            kernel=self.kernel,
            normalize_y=True,
            n_restarts_optimizer=10
        )
        
        # Initialize scalers
        self.x_scaler = StandardScaler()
        self.y_scaler = StandardScaler()
        
    def load_data(self, file_pattern):
        """
        Load data from multiple CSV files matching the pattern.
        
        Parameters:
        file_pattern (str): Pattern to match CSV files (e.g., "data/*.csv")
        
        Returns:
        tuple: Combined X (years) and y (values) arrays
        """
        all_data = []
        
        # Get list of all files matching the pattern
        files = glob.glob(file_pattern)
        
        for file in files:
            df = pd.read_csv(file)
            all_data.append(df)
            
        # Combine all dataframes
        combined_data = pd.concat(all_data, axis=0)
        
        # Extract years (assuming first column is years)
        years = combined_data.iloc[:, 0].values.reshape(-1, 1)
        
        # Extract values (all columns except first)
        values = combined_data.iloc[:, 1:].values
        
        return years, values
    
    def preprocess_data(self, X, y):
        """
        Preprocess the data by scaling.
        """
        X_scaled = self.x_scaler.fit_transform(X)
        y_scaled = self.y_scaler.fit_transform(y)
        return X_scaled, y_scaled
    
    def fit(self, X, y):
        """
        Fit the Gaussian Process model to the data.
        """
        # Preprocess the data
        X_scaled, y_scaled = self.preprocess_data(X, y)
        
        # Fit the model
        self.model.fit(X_scaled, y_scaled)
        
    def predict(self, X_new, return_std=True):
        """
        Make predictions with the trained model.
        
        Parameters:
        X_new: New input data points
        return_std: Whether to return standard deviation
        
        Returns:
        tuple: Predictions and optionally standard deviations
        """
        # Scale the input
        X_new_scaled = self.x_scaler.transform(X_new)
        
        # Make predictions
        if return_std:
            y_pred_scaled, std_scaled = self.model.predict(X_new_scaled, return_std=True)
            
            # Inverse transform predictions
            y_pred = self.y_scaler.inverse_transform(y_pred_scaled)
            
            # Scale the standard deviation back
            std = std_scaled * self.y_scaler.scale_
            
            return y_pred, std
        else:
            y_pred_scaled = self.model.predict(X_new_scaled)
            y_pred = self.y_scaler.inverse_transform(y_pred_scaled)
            return y_pred
    
    def plot_predictions(self, X, y, X_new=None):
        """
        Plot the original data and predictions.
        """
        if X_new is None:
            X_new = X
            
        # Make predictions
        y_pred, std = self.predict(X_new)
        
        plt.figure(figsize=(12, 6))
        
        # Plot original data
        plt.scatter(X, y, color='black', label='Observations')
        
        # Plot predictions
        plt.plot(X_new, y_pred, color='blue', label='Prediction')
        
        # Plot confidence intervals
        plt.fill_between(
            X_new.ravel(),
            y_pred.ravel() - 1.96 * std,
            y_pred.ravel() + 1.96 * std,
            color='blue',
            alpha=0.2,
            label='95% confidence interval'
        )
        
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.title('Gaussian Process Time Series Prediction')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage
if __name__ == "__main__":
    # Initialize the model
    gp_model = TimeSeriesGP(length_scale=1.0, noise_level=0.1)
    
    # Load data from multiple CSV files
    X, y = gp_model.load_data("data/*.csv")
    
    # Fit the model
    gp_model.fit(X, y)
    
    # Generate future dates for prediction
    future_years = np.linspace(X.min(), X.max() + 5, 100).reshape(-1, 1)
    
    # Plot the results
    gp_model.plot_predictions(X, y, future_years)