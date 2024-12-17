import base64
from io import BytesIO
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.metrics import mean_squared_error
from prophet import Prophet
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel

from flask import Flask, jsonify, send_file
from flask_cors import CORS

import warnings

app = Flask(__name__)
CORS(app)

warnings.filterwarnings('ignore')

# PAJAK
def ai_model_pajak():
    # Load and concatenate data
    dfs = []
    for i in range(1, 7):
        df = pd.read_csv(f'/home/litfan/Code/GIT/Cloud-Computing-Class/CC-LAFA/AI/data/Pajak/Realisasi Pendapatan Negara, {2007 + (i-1)*3}-{2009 + (i-1)*3}.csv')
        penerimaan_pajak = df[df.iloc[:, 0].str.strip() == 'Penerimaan Perpajakan'].iloc[:, 1:4]
        cleaned_df = pd.DataFrame({
            'Tahun': [str(year) for year in range(2007 + (i-1)*3, 2010 + (i-1)*3)],
            'Penerimaan Pajak': [str(value) for value in penerimaan_pajak.values.flatten()]
        })
        dfs.append(cleaned_df)

    data = pd.concat(dfs).reset_index(drop=True)
    data['Penerimaan Pajak'] = pd.to_numeric(data['Penerimaan Pajak'], errors='coerce').fillna(0)

    # LSTM Implementation
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data['Penerimaan Pajak'].values.reshape(-1, 1))

    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset) - look_back - 1):
            X.append(dataset[i:(i + look_back), 0])
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

    look_back = 3
    dataset = data_scaled
    train_size = int(len(dataset) * 0.67)
    train, test = dataset[0:train_size], dataset[train_size:]

    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

    # Enhanced LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    # Increased epochs
    model.fit(trainX, trainY, epochs=20, batch_size=1, verbose=0)

    # Adjust the predictions to extend until 2031 (7 years from 2024)
    future_years = [str(year) for year in range(2024, 2032)]

    # LSTM Implementation
    # Modified to predict 7 years ahead
    lstm_future = []
    last_sequence = data_scaled[-look_back:]
    last_sequence = np.reshape(last_sequence, (1, look_back, 1))

    for _ in range(7):  # Changed from 5 to 7 years
        next_pred = model.predict(last_sequence)
        lstm_future.append(next_pred[0,0])
        last_sequence = np.roll(last_sequence, -1)
        last_sequence[0,-1,0] = next_pred

    lstm_future = np.array(lstm_future).reshape(-1, 1)
    lstm_future = scaler.inverse_transform(lstm_future)


    # Prophet Implementation
    prophet_data = pd.DataFrame({
        'ds': pd.to_datetime(data['Tahun']),
        'y': data['Penerimaan Pajak']
    })

    prophet_model = Prophet(yearly_seasonality=True)
    prophet_model.fit(prophet_data)

    # Extend Prophet predictions to 2031
    future_dates = prophet_model.make_future_dataframe(periods=7, freq='Y')  # Changed from 5 to 7 years
    prophet_forecast = prophet_model.predict(future_dates)

    # Gaussian Process Implementation
    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(1, (1e-2, 1e2))
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

    # Fit the GP model
    X_train = np.arange(len(data)).reshape(-1, 1)
    y_train = data['Penerimaan Pajak'].values
    gp.fit(X_train, y_train)

    # Extend GP predictions to 2031
    X_pred = np.arange(len(data), len(data) + 7).reshape(-1, 1)  # Changed from 5 to 7 years
    y_pred, sigma = gp.predict(X_pred, return_std=True)
    X_pred = np.arange(len(data), len(data) + 7).reshape(-1, 1)  # Changed from 5 to 7 years
    y_pred, sigma = gp.predict(X_pred, return_std=True)

    # Plot predictions
    future_years = [str(year) for year in range(2024, 2031)]  # Updated range

    # Create interactive plot using Plotly
    fig = go.Figure()

    # Historical data trace
    fig.add_trace(go.Scatter(
        x=data['Tahun'],
        y=data['Penerimaan Pajak'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='black', width=2),
        marker=dict(size=8)
    ))

    # LSTM predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=lstm_future.flatten(),
        mode='lines+markers',
        name='LSTM Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='square', size=8)
    ))

    # Prophet predictions
    prophet_predictions = prophet_forecast['yhat'][-7:].values 

    # Prophet predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=prophet_predictions.flatten(),
        mode='lines+markers',
        name='Prophet Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='triangle-up', size=8)
    ))

    # Gaussian Process predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=y_pred.flatten(),
        mode='lines+markers',
        name='GP Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='diamond', size=8)
    ))

    # Calculate combined predictions
    combined_predictions = (lstm_future.flatten() + prophet_predictions + y_pred) / 3

    # Combined predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=combined_predictions.flatten(),
        mode='lines+markers',
        name='Combined Predictions',
        line=dict(color='red', width=2),
        marker=dict(size=8)
    ))

    # Update layout
    fig.update_layout(
        title={
            'text': 'Tax Revenue Predictions until 2031',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        xaxis_title='Year',
        yaxis_title='Tax Revenue (in Billions IDR)',
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.write_image(file=buf, format='png')
    # Embed the result in the html output.
    buf.seek(0)
    return buf

# APBN
def ai_model_apbn():
    # Load and concatenate data
    dfs = []
    for i in range(1, 7):
        df = pd.read_csv(f'./data/APBN/Tabel Anggaran Belanja Pemerintah Pusat Berdasarkan Fungsi, {2005 + (i-1)*3}-{2007 + (i-1)*3}.csv')
        penerimaan_pajak = df[df.iloc[:, 0].str.strip() == 'Jumlah'].iloc[:, 1:4]
        cleaned_df = pd.DataFrame({
            'Tahun': [str(year) for year in range(2007 + (i-1)*3, 2010 + (i-1)*3)],
            'APBN': [str(value) for value in penerimaan_pajak.values.flatten()]
        })
        dfs.append(cleaned_df)

    data = pd.concat(dfs).reset_index(drop=True)
    data['APBN'] = pd.to_numeric(data['APBN'], errors='coerce').fillna(0)

    # LSTM Implementation
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data['APBN'].values.reshape(-1, 1))

    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset) - look_back - 1):
            X.append(dataset[i:(i + look_back), 0])
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

    look_back = 3
    dataset = data_scaled
    train_size = int(len(dataset) * 0.67)
    train, test = dataset[0:train_size], dataset[train_size:]

    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

    # Enhanced LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    # Increased epochs
    model.fit(trainX, trainY, epochs=20, batch_size=1, verbose=0)

    # Adjust the predictions to extend until 2031 (7 years from 2024)
    future_years = [str(year) for year in range(2024, 2032)]

    # LSTM Implementation
    # Modified to predict 7 years ahead
    lstm_future = []
    last_sequence = data_scaled[-look_back:]
    last_sequence = np.reshape(last_sequence, (1, look_back, 1))

    for _ in range(7):  # Changed from 5 to 7 years
        next_pred = model.predict(last_sequence)
        lstm_future.append(next_pred[0,0])
        last_sequence = np.roll(last_sequence, -1)
        last_sequence[0,-1,0] = next_pred

    lstm_future = np.array(lstm_future).reshape(-1, 1)
    lstm_future = scaler.inverse_transform(lstm_future)


    # Prophet Implementation
    prophet_data = pd.DataFrame({
        'ds': pd.to_datetime(data['Tahun']),
        'y': data['APBN']
    })

    prophet_model = Prophet(yearly_seasonality=True)
    prophet_model.fit(prophet_data)

    # Extend Prophet predictions to 2031
    future_dates = prophet_model.make_future_dataframe(periods=7, freq='Y')  # Changed from 5 to 7 years
    prophet_forecast = prophet_model.predict(future_dates)

    # Gaussian Process Implementation
    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(1, (1e-2, 1e2))
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

    # Fit the GP model
    X_train = np.arange(len(data)).reshape(-1, 1)
    y_train = data['APBN'].values
    gp.fit(X_train, y_train)

    # Extend GP predictions to 2031
    X_pred = np.arange(len(data), len(data) + 7).reshape(-1, 1)  # Changed from 5 to 7 years
    y_pred, sigma = gp.predict(X_pred, return_std=True)
    X_pred = np.arange(len(data), len(data) + 7).reshape(-1, 1)  # Changed from 5 to 7 years
    y_pred, sigma = gp.predict(X_pred, return_std=True)

    # Plot predictions
    future_years = [str(year) for year in range(2024, 2031)]  # Updated range

    # Create interactive plot using Plotly
    fig = go.Figure()

    # Historical data trace
    fig.add_trace(go.Scatter(
        x=data['Tahun'],
        y=data['APBN'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='black', width=2),
        marker=dict(size=8)
    ))

    # LSTM predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=lstm_future.flatten(),
        mode='lines+markers',
        name='LSTM Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='square', size=8)
    ))

    # Prophet predictions
    prophet_predictions = prophet_forecast['yhat'][-7:].values 

    # Prophet predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=prophet_predictions.flatten(),
        mode='lines+markers',
        name='Prophet Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='triangle-up', size=8)
    ))

    # Gaussian Process predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=y_pred.flatten(),
        mode='lines+markers',
        name='GP Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='diamond', size=8)
    ))

    # Calculate combined predictions
    combined_predictions = (lstm_future.flatten() + prophet_predictions + y_pred) / 3

    # Combined predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=combined_predictions.flatten(),
        mode='lines+markers',
        name='Combined Predictions',
        line=dict(color='red', width=2),
        marker=dict(size=8)
    ))

    # Update layout
    fig.update_layout(
        title={
            'text': 'APBN Predictions until 2031',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        xaxis_title='Year',
        yaxis_title='APBN (in Billions IDR)',
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.write_image(file=buf, format='png')
    # Embed the result in the html output.
    buf.seek(0)
    return buf

# PDB
def ai_model_pdb():
    # Load and concatenate data
    dfs = []
    for i in range(1, 15):
        df = pd.read_csv(f'./data/PDB/[Seri 2010] 2. PDB Triwulanan Atas Dasar Harga Konstan menurut Pengeluaran, {2010 + (i-1)}.csv')
        pdb = df[df.iloc[:, 0].str.contains('8. PRODUK DOMESTIK BRUTO', na=False)].iloc[:, 5]
        cleaned_df = pd.DataFrame({
            'Tahun': [str(2010 + (i-1))],
            'PDB': [str(value) for value in pdb.values.flatten()]
        })
        dfs.append(cleaned_df)

    data = pd.concat(dfs).reset_index(drop=True)
    data['PDB'] = pd.to_numeric(data['PDB'], errors='coerce').fillna(0)

    # LSTM Implementation
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data['PDB'].values.reshape(-1, 1))

    def create_dataset(dataset, look_back=1):
        X, Y = [], []
        for i in range(len(dataset) - look_back - 1):
            X.append(dataset[i:(i + look_back), 0])
            Y.append(dataset[i + look_back, 0])
        return np.array(X), np.array(Y)

    look_back = 3
    dataset = data_scaled
    train_size = int(len(dataset) * 0.67)
    train, test = dataset[0:train_size], dataset[train_size:]

    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

    # Enhanced LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    # Increased epochs
    model.fit(trainX, trainY, epochs=20, batch_size=1, verbose=0)

    # Adjust the predictions to extend until 2031 (7 years from 2024)
    future_years = [str(year) for year in range(2024, 2032)]

    # LSTM Implementation
    # Modified to predict 7 years ahead
    lstm_future = []
    last_sequence = data_scaled[-look_back:]
    last_sequence = np.reshape(last_sequence, (1, look_back, 1))

    for _ in range(7):  # Changed from 5 to 7 years
        next_pred = model.predict(last_sequence)
        lstm_future.append(next_pred[0,0])
        last_sequence = np.roll(last_sequence, -1)
        last_sequence[0,-1,0] = next_pred

    lstm_future = np.array(lstm_future).reshape(-1, 1)
    lstm_future = scaler.inverse_transform(lstm_future)


    # Prophet Implementation
    prophet_data = pd.DataFrame({
        'ds': pd.to_datetime(data['Tahun']),
        'y': data['PDB']
    })

    prophet_model = Prophet(yearly_seasonality=True)
    prophet_model.fit(prophet_data)

    # Extend Prophet predictions to 2031
    future_dates = prophet_model.make_future_dataframe(periods=7, freq='Y')  # Changed from 5 to 7 years
    prophet_forecast = prophet_model.predict(future_dates)

    # Gaussian Process Implementation
    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(1, (1e-2, 1e2))
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

    # Fit the GP model
    X_train = np.arange(len(data)).reshape(-1, 1)
    y_train = data['PDB'].values
    gp.fit(X_train, y_train)

    # Extend GP predictions to 2031
    X_pred = np.arange(len(data), len(data) + 7).reshape(-1, 1)  # Changed from 5 to 7 years
    y_pred, sigma = gp.predict(X_pred, return_std=True)
    X_pred = np.arange(len(data), len(data) + 7).reshape(-1, 1)  # Changed from 5 to 7 years
    y_pred, sigma = gp.predict(X_pred, return_std=True)

    # Plot predictions
    future_years = [str(year) for year in range(2024, 2031)]  # Updated range

    # Create interactive plot using Plotly
    fig = go.Figure()

    # Historical data trace
    fig.add_trace(go.Scatter(
        x=data['Tahun'],
        y=data['PDB'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='black', width=2),
        marker=dict(size=8)
    ))

    # LSTM predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=lstm_future.flatten(),
        mode='lines+markers',
        name='LSTM Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='square', size=8)
    ))

    # Prophet predictions
    prophet_predictions = prophet_forecast['yhat'][-7:].values 

    # Prophet predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=prophet_predictions.flatten(),
        mode='lines+markers',
        name='Prophet Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='triangle-up', size=8)
    ))

    # Gaussian Process predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=y_pred.flatten(),
        mode='lines+markers',
        name='GP Predictions',
        line=dict(dash='dash', width=2),
        marker=dict(symbol='diamond', size=8)
    ))

    # Calculate combined predictions
    combined_predictions = (lstm_future.flatten() + prophet_predictions + y_pred) / 3

    # Combined predictions trace
    fig.add_trace(go.Scatter(
        x=future_years,
        y=combined_predictions.flatten(),
        mode='lines+markers',
        name='Combined Predictions',
        line=dict(color='red', width=2),
        marker=dict(size=8)
    ))

    # Update layout
    fig.update_layout(
        title={
            'text': 'PDB Predictions until 2031',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        xaxis_title='Year',
        yaxis_title='PDB (in Billions IDR)',
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.write_image(file=buf, format='png')
    # Embed the result in the html output.
    buf.seek(0)
    return buf

@app.route('/ai/pajak', methods=['GET'])
def get_prediction():
    try:
        return send_file(ai_model_pajak(), mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/ai/apbn', methods=['GET'])
def get_prediction2():
    try:
        return send_file(ai_model_apbn(), mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai/pdb', methods=['GET'])
def get_prediction3():
    try:
        return send_file(ai_model_pdb(), mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3001, debug=True)