#TODO: Swichting to deep learning model
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def train_f1_model_from_dataframes(data_list):
    # 1. Combine the list of DataFrames into a single DataFrame
    all_race_data = pd.concat(data_list, ignore_index=True)

    # 2. Data Preprocessing
    # Handle missing data (e.g., forward fill missing values)
    all_race_data = all_race_data.fillna(method="ffill")
    
    # Feature scaling (e.g., Practice sessions, Qualifying, Driver Points)
    scaler = MinMaxScaler()
    numeric_columns = ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Driver Points', 'Constructor Points']  # Adjust columns as needed
    all_race_data[numeric_columns] = scaler.fit_transform(all_race_data[numeric_columns])

    # Categorical encoding (e.g., Constructor column)
    all_race_data = pd.get_dummies(all_race_data, columns=['Constructor'])  # Adjust columns as needed

    # 3. Split data into features (X) and target (y)
    X = all_race_data.drop(columns=['Final Race Position'])  # Features
    y = all_race_data['Final Race Position']  # Target variable

    # 4. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Convert data to NumPy arrays
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    # 5. Build the Deep Learning Model
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))  # Input layer
    model.add(Dense(128, activation='relu'))  # Hidden layer
    model.add(Dropout(0.2))  # Dropout to prevent overfitting
    model.add(Dense(64, activation='relu'))  # Hidden layer
    model.add(Dense(1, activation='linear'))  # Output layer (regression)

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # 6. Train the Model
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    # 7. Evaluate the Model
    loss, mae = model.evaluate(X_test, y_test)
    print(f"Test Loss: {loss}")
    print(f"Test MAE: {mae}")

    # Return the trained model and training history
    return model, history
