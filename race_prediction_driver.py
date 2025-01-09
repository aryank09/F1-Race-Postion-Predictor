import race_prediction_calculator as prdctr

if __name__ == "__main__":
    print("Welcome to the F1 Race Results predictor!")
    
    #Get user input for the race name
    race_name = input("Enter the race name: ").strip()

    print(prdctr.prediction_driver(race_name))

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