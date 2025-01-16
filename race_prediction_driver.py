#Description: This is the driver program to run the project
#Author: Aryan Khanna
#Version: Jan 9th, 2025

import race_prediction_calculator as data_collection
import race_prediction_model as prdctr

if __name__ == "__main__":
    print("Welcome to the F1 Race Results predictor!")
    
    #Get user input for the race name
    race_name = input("Enter the race name: ").strip()

    data = data_collection.data_compiler_new(race_name)

    current_data = data_collection.current_race_data(race_name)

    print(data)
    current_race_data_list = [current_data]
    

    trained_model, trained_scaler = prdctr.train_f1_model(data)
    top_5 = prdctr.predict_top_5(current_data, trained_model, trained_scaler)
    print("Top 5 Predicted Drivers in conetention for winning are:")
    print(top_5)
    
