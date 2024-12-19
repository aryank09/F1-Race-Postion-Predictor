import temp_race_prediction_calculator as prdctr

if __name__ == "__main__":
    print("Welcome to the F1 Results URL Generator!")
    
    # Get user input for the race name
    race_name = input("Enter the race name: ").strip()

    prdctr.prediction_driver(race_name)