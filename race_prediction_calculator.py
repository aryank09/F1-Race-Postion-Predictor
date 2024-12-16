import f1_results_scraper as scrpr

results1 = scrpr.result_scraper("https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/1")
results2 = scrpr.result_scraper("https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/2")
results3 = scrpr.result_scraper("https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/3")

#TODO: 
#format example ['LandoNorrisNOR', 'McLaren Mercedes', '1:24.542']
#keep in mind time is str
#keep in mind since practice session other drivers may be present than racing
#so we have to add their time and divide it by the times they were in the practice session instead of 3
print(results1)