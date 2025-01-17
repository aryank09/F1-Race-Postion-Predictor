#Description: This program compiles the data and performs the necessary actions needed to performed to make ready for the
#prediction model
#Author: Aryan Khanna
#Version: Jan 9th, 2025

import f1_results_scraper as scrpr
import pandas as pd

#format example ['LandoNorrisNOR', 'McLaren Mercedes', '1:24.542']
#keep in mind time is str
#keep in mind since practice session other drivers may be present than racing
#so we have to add their time and divide it by the times they were in the practice session instead of 3

#race ids to build the url
race_id_mapping = {
    "bahrain": 1229,
    "saudi-arabia": 1230,
    "australia": 1231,
    "azerbaijan": 1245,
    "emilia-romagna": 1235,
    "monaco": 1236,
    "spain": 1238,
    "canada": 1237,
    "great-britain": 1240,
    "hungary": 1241,
    "belgium": 1242,
    "netherlands": 1243,
    "italy": 1244,
    "singapore": 1246,
    "japan": 1232,
    "mexico": 1248,
    "las-vegas": 1250,
    "abu-dhabi": 1252
    }

#driver IDs to map theier driver number for identifying
drivers = {
        "MaxVerstappenVER": 1,
        "LandoNorrisNOR": 4,
        "CharlesLeclercLEC": 16,
        "OscarPiastriPIA": 81,
        "CarlosSainzSAI": 55,
        "GeorgeRussellRUS": 63,
        "LewisHamiltonHAM": 44,
        "SergioPerezPER": 11,
        "FernandoAlonsoALO": 14,
        "PierreGaslyGAS": 10,
        "NicoHulkenbergHUL": 27,
        "YukiTsunodaTSU": 22,
        "LanceStrollSTR": 18,
        "EstebanOconOCO": 31,
        "KevinMagnussenMAG": 20,
        "AlexanderAlbonALB": 23,
        "DanielRicciardoRIC": 3,
        "OliverBearmanBEA": 87,
        "FrancoColapintoCOL": 43,
        "ZhouGuanyuZHO": 24,
        "LiamLawsonLAW": 30,
        "ValtteriBottasBOT": 77,
        "LoganSargeantSAR": 2,
        "JackDoohanDOO": 7,
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
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/starting-grid"


#data_compiler methods
#Description: This the main driver function responsible for compiling the data
#
#PRE-CONDTIONS: The race weekend name should be valid otherwise it will give error message
#
#POST-CONDITIONS: Results are compilied 
#
#@params race_weekend_name is a str
#@return total_results is a dictionary 
def data_compiler(race_weekend_name):
    total_results = {}
    session_labels = ["Practice 1", "Practice 2", "Practice 3", "Qualifying"]
    driver_points = scrpr.driver_points_scraper(race_weekend_name)
    constructor_points = scrpr.constructors_points_scraper(race_weekend_name)
    race_results = scrpr.race_result_position_scraper(race_weekend_name)
    for session_number in range(1, 5):
        session_results = scrpr.result_scraper(build_f1_url(race_weekend_name, session_number))
        
        for result in session_results:
            driver_name = result[0]
            constructor_name = result[1]

            #Adding session timing or position
            if session_number < 5:  # For practice and qualifying
                time_str = result[2]
                session_data = time_in_seconds(time_str)
            else:#For race result
                session_data = int(result[3]) if result[3].isdigit() else None

            if driver_name not in total_results:
                #Initializing driver entry with default None values for all sessions
                total_results[driver_name] = {
                    "Constructor": constructor_name,
                    "Grand Prix": race_weekend_name.lower().replace(" ", "-"),
                    session_labels[0]: None,
                    session_labels[1]: None,
                    session_labels[2]: None,
                    session_labels[3]: None
                }
            
            #Updating the session data
            total_results[driver_name][session_labels[session_number - 1]] = session_data
            
            if driver_name in drivers:
                total_results[driver_name]["Driver ID"] = drivers[driver_name]

            if driver_name in driver_points:
                total_results[driver_name]["Driver Points"] = driver_points[driver_name]

            if constructor_name in constructor_points:
                total_results[driver_name]["Constructor Points"] = constructor_points[constructor_name]
            
            if driver_name in race_results:
                total_results[driver_name]["Race Finish Position"] = race_results[driver_name]
            


    return required_data(total_results)

#requried_data method
#
#Description: This method compiles results and restructures it usings pandas as dataframes
#
#PRE-CONDTIONS: results should be dictionary
#
#POST-CONDITIONS: The results are returned in the list of df
#
#@params results is a dictionary
#@return df_sorted is a dataframe

def required_data(results):
    df = pd.DataFrame.from_dict(results, orient='index')
    
    #Converting 'Race Finish Position' to numeric, treating 'NC' and 'DQ' as NaN
    df['Race Finish Position'] = pd.to_numeric(df['Race Finish Position'], errors='coerce')
    
    # Sort the DataFrame by 'Race Finish Position' in ascending order
    df_sorted = df.sort_values(by='Race Finish Position')

    cols = [col for col in df_sorted.columns if col != 'Race Finish Position']
    df_sorted = df_sorted[cols[:1] + ['Race Finish Position'] + cols[1:]]
    df_sorted = df_sorted.fillna(0)
    return df_sorted

#data_compiler_new method
#
#Description: This method compiles races results upto the weekend entered by the user
#
#PRE-CONDTIONS: race_weekend_name should be spelt correctly
#
#POST-CONDITIONS: The results are returned in the list of df
#
#@params race_weekend_name is a str
#@return result is a list

def data_compiler_new(race_weekend_name):
    result = []

    grandprix = [
    "bahrain", "saudi-arabia", "australia", "japan",  "emilia-romagna", "monaco",
     "canada", "spain", "great-britain", "hungary", "belgium", "netherlands", "italy", "azerbaijan",
    "singapore", "mexico", "las-vegas", "abu-dhabi"]

    i = 0

    race_weekend_name = race_weekend_name.lower().replace(" ", "-")

    while grandprix[i] != race_weekend_name:
        result.append(data_compiler(grandprix[i]))
        i += 1
    
    return result

#current_race_data method
#
#Description: This method compiles races results  positions upto the weekend entered by the user
#
#PRE-CONDTIONS: race_weekend_name should be spelt correctly
#
#POST-CONDITIONS: The results are returned in the list of df
#
#@params race_weekend_name is a str
#@return result is a list
def current_race_data(race_weekend_name):
    data = data_compiler(race_weekend_name)
    data = data.drop(columns=['Race Finish Position', 'Grand Prix'], inplace=False)
    return data