import temp_race_prediction_calculator as prdctr

if __name__ == "__main__":
    print("Welcome to the F1 Race Results predictor!")
    
    #Get user input for the race name
    race_name = input("Enter the race name: ").strip()

    prdctr.prediction_driver(race_name)

#isssues with the following races
#saudi arabia
#japan
#china(sprint)
#miami(sprint)
#emilia romagna (issue with scrpr) - fixed!
#monaco
#canada
#spain
#austria(sprint)
#great britain (issue with scrpr) - fixed!
#hungary
#netherlands
#italy
#azerbaijan
#united-states(sprint)
#mexico
#brazil(sprint)
#qatar(sprint)