#Description: This is the driver program to run the project
#Author: Aryan Khanna
#Version: Jan 9th, 2025

import race_prediction_calculator as data_collection
import race_prediction_model as prdctr

if __name__ == "__main__":
    print("Welcome to the F1 Race Results predictor!")
    
    #Get user input for the race name
    race_name = input("Enter the race name: ").strip()

    data = data_collection.data_compiler(race_name)

    print(data)

    #prdctr.predict_race_finish_position(data)


#not for sprint weekends