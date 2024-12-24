import f1_results_scraper as scrpr

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

def find_string_index(target, total_results):
    for outer_index, inner_list in enumerate(total_results):
        if target in inner_list:
            return outer_index
    return None

def time_in_seconds(time_str):
    if len(time_str) != 0:
        minutes, seconds = map(float, time_str.split(":"))
        total_seconds = minutes * 60 + seconds
        return total_seconds
    else:
        return 0

def format_time(seconds):
        minutes = int(seconds // 60)  
        remaining_seconds = seconds % 60  
        return f"{minutes}:{remaining_seconds:06.3f}"

def format_prediction(sorted_prediction): 
    for result in sorted_prediction:
        if isinstance(result[2], (int, float)):
            result[2] = format_time(result[2])

    return sorted_prediction


def predictor(total_results):
    prediction = []
    for i in range(len(total_results)):
        temp = []
        temp.append(total_results[i][0])
        temp.append(total_results[i][1])
        predicted_time = total_results[i][2]/total_results[i][3]
        temp.append(predicted_time)
        prediction.append(temp)
    return prediction

def build_f1_url(race_name, session_number):
    race_name_key = race_name.lower().replace(" ", "-")
    
    #Get race ID from the dictionary
    race_id = race_id_mapping.get(race_name_key)
    
    if not race_id:
        return None 

    #Construct and return the URL
    if(session_number == 1 or session_number == 2 or session_number == 3):
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/practice/{session_number}"
    else:
        return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/starting-grid/{session_number}"   

def prediction_driver(race_weekend_name):

    total_results = []

    driver_name = set()

    for x in range(1,5):
        results = scrpr.result_scraper(build_f1_url(race_weekend_name,x))
        for i in range(len(results)):
            if results[i][0] not in driver_name:
                total_seconds = time_in_seconds(results[i][2])
                results[i][2] = total_seconds
                count = 1
                results[i].append(count)
                total_results.append(results[i])
                driver_name.add(results[i][0]) 
            else:
                outer_index = find_string_index(results[i][0],total_results)
                if outer_index is not None:
                    total_seconds = time_in_seconds(results[i][2])
                    if total_seconds != 0:
                        total_results[outer_index][2] += total_seconds
                        total_results[outer_index][3] += 1

    prediction = predictor(total_results)
    sorted_prediction = sorted(prediction, key=lambda x: (x[2] == 0, x[2]))
    formated_prediction = format_prediction(sorted_prediction)
    for index, result in enumerate(formated_prediction, start=1):
        print(f"{index}. {result}")