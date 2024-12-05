import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load and combine CSV files
file_paths = [
    './data/Realisasi Pendapatan Negara, 2007-2009.csv',
    './data/Realisasi Pendapatan Negara, 2010-2012.csv',
    './data/Realisasi Pendapatan Negara, 2013-2015.csv',
    './data/Realisasi Pendapatan Negara, 2016-2018.csv',
    './data/Realisasi Pendapatan Negara, 2019-2021.csv',
    './data/Realisasi Pendapatan Negara, 2022-2024.csv'
]

data_frames = [pd.read_csv(file, skiprows=3) for file in file_paths]
data = pd.concat(data_frames, ignore_index=True)

# Step 2: Preprocess the data
# Transpose the DataFrame if the target data is in a row
data = data.T

# Set the first row as the header
data.columns = data.iloc[0]
data = data[1:]

# Convert all columns to numeric, forcing non-numeric values to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Fill missing values with mean
data.fillna(data.mean(), inplace=True)

# Step 3: Visualize the data
# Create a table
print(data)

# Plot the data
plt.figure(figsize=(14, 8))

# Plot each column
for column in data.columns:
    plt.plot(data.index, data[column], label=column)

plt.xlabel('Year')
plt.ylabel('Value (Milyar Rupiah)')
plt.title('Realisasi Pendapatan Negara')
plt.legend()
plt.grid(True)
plt.show()