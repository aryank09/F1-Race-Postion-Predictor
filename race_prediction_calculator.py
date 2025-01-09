#Description: This program compiles the data and performs the necessary actions needed to performed to make ready for the
#prediction model
#Author: Aryan Khanna
#Version: Jan 9th, 2025

import f1_results_scraper as scrpr

#format example ['LandoNorrisNOR', 'McLaren Mercedes', '1:24.542']
#keep in mind time is str
#keep in mind since practice session other drivers may be present than racing
#so we have to add their time and divide it by the times they were in the practice session instead of 3

#race ids to build the url
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

#time_in_seconds methods
#Description: This method takes the avalible time in str format and converts it to seconds
#
#PRE-CONDTIONS: The parameter should be a string
#
#POST-CONDITIONS: Time is converted into seconds
#
#@params time_str is a str
#@return float
def time_in_seconds(time_str):
    #Converting time from 'm:ss.mmm' to seconds.
    if time_str:
        minutes, seconds = map(float, time_str.split(":"))
        return minutes * 60 + seconds
    return None

#build_f1_url methods
#Description: This method build the url for web scrapping
#
#PRE-CONDTIONS: The parameter should be a string being the race name in correct spelling with the session number being 1-4
#
#POST-CONDITIONS: url is built
#
#@params race_name, is a str and session_number is a int
#@return str
def build_f1_url(race_name, session_number):
    #Building URL for scraping F1 results.
    race_name_key = race_name.lower().replace(" ", "-")
    race_id = race_id_mapping.get(race_name_key)
    if not race_id:
        return None
    if session_number in [1, 2, 3]:
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/practice/{session_number}"
    elif session_number == 4:
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/starting-grid/4"

#get_driver_points methods
#Description: Building in progress
#
#PRE-CONDTIONS: 
#
#POST-CONDITIONS: 
#
#@params 
#@return 
def get_driver_points(race_name):
    driver_points = {}

    #for temporary measure we are going to scrape results from driver pages and add them up

    race_name_mapping = [
        "bahrain",
        "saudi-arabia",
        "australia",
        "azerbaijan",
        "miami",
        "emilia-romagna",
        "monaco",
        "spain",
        "canada",
        "austria",
        "great-britain",
        "hungary",
        "belgium",
        "netherlands",
        "italy",
        "singapore",
        "japan",
        "qatar",
        "united-states",
        "mexico",
        "brazil",
        "las-vegas",
        "abu-dhabi"
    ]

    upper_limit = race_name_mapping.index(race_name)

    for i in range(0, upper_limit):
        #temp
        #TODO: write the loop for adding driver points for the respective weekend limit to get total driver points
        return None

    return driver_points

#prediction_driver methods
#Description: This the main driver function responisble fro compiling the data
#
#PRE-CONDTIONS: The race weekend name should be valid otherwise it will give error message
#
#POST-CONDITIONS: Results are compilied 
#
#@params race_weekend_name is a str
#@return total_results is a dictionary 
def prediction_driver(race_weekend_name):
    total_results = {}
    session_labels = ["Practice 1", "Practice 2", "Practice 3", "Qualifying"]
    driver_points = get_driver_points(race_weekend_name)
    for session_number in range(1, 5):
        session_results = scrpr.result_scraper(build_f1_url(race_weekend_name, session_number))
        
        for result in session_results:
            driver_name = result[0]
            team_name = result[1]

            #Adding session timing or position
            if session_number < 5:  # For practice and qualifying
                time_str = result[2]
                session_data = time_in_seconds(time_str)
            else:#For race result
                session_data = int(result[3]) if result[3].isdigit() else None

            if driver_name not in total_results:
                #Initializing driver entry with default None values for all sessions
                total_results[driver_name] = {
                    "team": team_name,
                    session_labels[0]: None,
                    session_labels[1]: None,
                    session_labels[2]: None,
                    session_labels[3]: None,
                }
            
            #Updating the session data
            total_results[driver_name][session_labels[session_number - 1]] = session_data
            if driver_name in driver_points:
                total_results[driver_name]["Driver Points"] = driver_points[driver_name]
 

    return total_results

