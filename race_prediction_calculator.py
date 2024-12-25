import f1_results_scraper as scrpr
import csv

#format example ['LandoNorrisNOR', 'McLaren Mercedes', '1:24.542']
#keep in mind time is str
#keep in mind since practice session other drivers may be present than racing
#so we have to add their time and divide it by the times they were in the practice session instead of 3

race_id_mapping = {
    "bahrain": 1229,
    "saudi-arabia": 1230,
    "australia": 1231,
    "azerbaijan": 1232,
    "miami": 1233,
    "emilia-romagna": 1234,
    "monaco": 1235,
    "spain": 1236,
    "canada": 1237,
    "austria": 1238,
    "great-britain": 1239,
    "hungary": 1240,
    "belgium": 1241,
    "netherlands": 1242,
    "italy": 1243,
    "singapore": 1244,
    "japan": 1245,
    "qatar": 1246,
    "united-states": 1247,
    "mexico": 1248,
    "brazil": 1249,
    "las-vegas": 1250,
    "abu-dhabi": 1252
}

def time_in_seconds(time_str):
    """Convert time from 'm:ss.mmm' to seconds."""
    if time_str:
        minutes, seconds = map(float, time_str.split(":"))
        return minutes * 60 + seconds
    return None

def build_f1_url(race_name, session_number):
    """Build URL for scraping F1 results."""
    race_name_key = race_name.lower().replace(" ", "-")
    race_id = race_id_mapping.get(race_name_key)
    if not race_id:
        return None
    if session_number in [1, 2, 3]:
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/practice/{session_number}"
    elif session_number == 4:
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/starting-grid/4"
    elif session_number == 5:
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/race-result"

# Main driver function
def prediction_driver(race_weekend_name):
    """
    Gather F1 data for a race weekend and structure it into
    driverName, teamName, practice1, practice2, practice3, qualifying, finalPosition.
    """
    total_results = {}
    session_labels = ["Practice 1", "Practice 2", "Practice 3", "Qualifying", "Final Position"]

    for session_number in range(1, 6):
        session_results = scrpr.result_scraper(build_f1_url(race_weekend_name, session_number))
        
        for result in session_results:
            driver_name = result[0]
            team_name = result[1]

            # Add session timing or position
            if session_number < 5:  # For practice and qualifying
                time_str = result[2]
                session_data = time_in_seconds(time_str)
            else:  # For race result
                session_data = int(result[3]) if result[3].isdigit() else None

            if driver_name not in total_results:
                # Initialize driver entry with default None values for all sessions
                total_results[driver_name] = {
                    "team": team_name,
                    session_labels[0]: None,
                    session_labels[1]: None,
                    session_labels[2]: None,
                    session_labels[3]: None,
                    session_labels[4]: None
                }
            
            # Update the session data
            total_results[driver_name][session_labels[session_number - 1]] = session_data

    # Save results to CSV
    save_results_to_csv(total_results, file_name=f"{race_weekend_name}_results.csv")

def save_results_to_csv(total_results, file_name="f1_results.csv"):
    """
    Save the structured F1 results to a CSV file.
    """
    headers = ["Driver Name", "Team", "Practice 1", "Practice 2", "Practice 3", "Qualifying", "Final Position"]
    
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for driver_name, data in total_results.items():
            row = [
                driver_name,
                data["team"],
                data["Practice 1"],
                data["Practice 2"],
                data["Practice 3"],
                data["Qualifying"],
                data["Final Position"]
            ]
            writer.writerow(row)

    print(f"Results have been successfully saved to {file_name}")