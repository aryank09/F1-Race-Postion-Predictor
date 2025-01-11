#Description: This is the driver program to run the project
#Author: Aryan Khanna
#Version: Jan 9th, 2025

import race_prediction_calculator as data_collection
import race_prediction_model as prdctr

if __name__ == "__main__":
    print("Welcome to the F1 Race Results predictor!")
    
    #Get user input for the race name
    race_name = input("Enter the race name: ").strip()

    data = data_collection.prediction_driver(race_name)

    print(data)

    prdctr.main(data)


#isssues with the following races
#japan - issue with ocon being fastest avg
#china(sprint)
#miami(sprint)
#canada - logci error with 3 drivers being the fasts, which is not the case
#austria(sprint)
#netherlands - issue with ocon
#united-states(sprint)
#brazil(sprint)
#qatar(sprint)