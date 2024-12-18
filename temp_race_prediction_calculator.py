import f1_results_scraper as scrpr

#format example ['LandoNorrisNOR', 'McLaren Mercedes', '1:24.542']
#keep in mind time is str
#keep in mind since practice session other drivers may be present than racing
#so we have to add their time and divide it by the times they were in the practice session instead of 3

def find_string_index(target):
    for outer_index, inner_list in enumerate(total_results):
        if target in inner_list:
            return outer_index
    return None

def time_in_seconds(time_str):
    minutes, seconds = map(float, time_str.split(":"))
    total_seconds = minutes * 60 + seconds
    return total_seconds

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

results1 = scrpr.result_scraper("https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/1")
results2 = scrpr.result_scraper("https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/2")
results3 = scrpr.result_scraper("https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/3")
results4 = scrpr.result_scraper("https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/starting-grid")

total_results = []

driver_name = set()

for x in range(1,5):
    results = eval(f"results{x}") if f"results{x}" in globals() else []
    for i in range(len(results)):
        if results[i][0] not in driver_name:
            total_seconds = time_in_seconds(results[i][2])
            results[i][2] = total_seconds
            count = 1
            results[i].append(count)
            total_results.append(results[i])
            driver_name.add(results[i][0]) 
        else:
            outer_index = find_string_index(results[i][0])
            if outer_index is not None:
                total_seconds = time_in_seconds(results[i][2])
                total_results[outer_index][2] += total_seconds
                total_results[outer_index][3] += 1

prediction = predictor(total_results)
sorted_prediction = sorted(prediction, key=lambda x: x[2])
formated_prediction = format_prediction(sorted_prediction)
for index, result in enumerate(formated_prediction, start=1):
    print(f"{index}. {result}")