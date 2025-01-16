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
    
    #running the prediction model
    #prdctr.predict_next_grand_prix_position(data, current_race_data_list)


#not for sprint weekends