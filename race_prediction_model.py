import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Dropout

#race result from bahrain
drivers_result_key = {
    'MaxVerstappenVER': 1,
    'SergioPerezPER': 2,
    'CarlosSainzSAI': 3,
    'CharlesLeclercLEC': 4,
    'GeorgeRussellRUS': 5,
    'LandoNorrisNOR': 6,
    'LewisHamiltonHAM': 7,
    'OscarPiastriPIA': 8,
    'FernandoAlonsoALO': 9,
    'LanceStrollSTR': 10,
    'ZhouGuanyuZHO': 11,
    'KevinMagnussenMAG': 12,
    'DanielRicciardoRIC': 13,
    'YukiTsunodaTSU': 14,
    'AlexanderAlbonALB': 15,
    'NicoHulkenbergHUL': 16,
    'EstebanOconOCO': 17,
    'PierreGaslyGAS': 18,
    'ValtteriBottasBOT': 19,
    'LoganSargeantSAR': 20
}

#train_f1_model method
#
#Description: This method takes the data in the form of a list and trains a model using deep learning from tensorflow keras
#it also prints the loss and mae to give an idea of how accurate the model is.
#
#PRE-CONDITONS: The data should be a list of dataframes and the reuired modules should be present
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

#predict_top_5 method
#
#Description: This method uses the trained model to carry out predictions, with the help of the current race data
#(excluding the race finish position, because that has to be predicted)
#
#PRE-CONDITION: This method requires the trained model, along with the required packages installed
#
#POST-CONDITIONS: Top 5 contenders for the race win are predicted
#
#@params current_race_data is dataframe, model and scalar are data from using tf_keras
#@return formated_output is str

def predict_top_5(current_race_data, model, scaler):
    #Checking if the required columns exist in the data
    required_columns = ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Driver Points']
    for col in required_columns:
        if col not in current_race_data.columns:
            raise ValueError(f"Missing required column: {col}")

    #Scaling the input features using the provided scaler
    scaled_data = scaler.transform(current_race_data[required_columns])

    #Predicting race finish positions
    predicted_positions = model.predict(scaled_data).flatten()

    #Combining driver indices with predictions
    driver_predictions = list(enumerate(predicted_positions, start=1))  

    #Sorting by predicted positions (ascending) and get the top 5
    top_5_drivers = sorted((dp for dp in driver_predictions if dp[1] >= 0), key=lambda x: x[1])[:5]
    
    #Reversing the dictionary to map positions to driver names
    position_to_driver = {value: key for key, value in drivers_result_key.items()}

    #Mapping the positions in the predictions to driver names
    top_5_drivers_with_names = [(position_to_driver.get(pred[0], "Unknown Driver"), pred[1]) for pred in top_5_drivers]

    formatted_output = ', '.join(driver[0] for driver in top_5_drivers_with_names)

    return formatted_output