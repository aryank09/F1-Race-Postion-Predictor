import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Dropout

#train_f1_model method
#
#Description: This method takes the data in the form of a list and trains a model using deep learning from tensorflow keras
#it also prints the loss and mae to give an idea of how accurate the model is.
#
#PRE-CONDITONS: The data should be a list of dataframes
#
#POST-CONDITIONS: The model is trained
#
#@params data_list is a list of dataframes
#@return model, scalaar 
def train_f1_model(data_list):
    #combing the list of dataframes into single datafram
    all_race_data = pd.concat(data_list, ignore_index=True)

    #Feature scaling (e.g., Practice sessions, Qualifying, Driver Points)
    scaler = MinMaxScaler()
    numeric_columns = ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Driver Points']
    all_race_data[numeric_columns] = scaler.fit_transform(all_race_data[numeric_columns])

    #Spiltting in X and Y (Y is the target variable)
    X = all_race_data[numeric_columns]  
    y = all_race_data['Race Finish Position']  

    #Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Converting data to NumPy arrays
    X_train = np.array(X_train, dtype=np.float32)
    y_train = np.array(y_train, dtype=np.float32)
    X_test = np.array(X_test, dtype=np.float32)
    y_test = np.array(y_test, dtype=np.float32)

    #Building the Deep Learning Model
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))  #Input layer
    model.add(Dense(128, activation='relu'))  #Hidden layer
    model.add(Dropout(0.2))  #Dropout to prevent overfitting
    model.add(Dense(64, activation='relu'))  #Hidden layer
    model.add(Dense(1, activation='linear'))  #Output layer (regression)

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    #Traing the model
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    #Eval the model
    loss, mae = model.evaluate(X_test, y_test)
    print(f"Test Loss: {loss}")
    print(f"Test MAE: {mae}")

    return model, scaler

