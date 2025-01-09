#Description: This program uses requests and BeautifulSoup to scrape websites to get f1 results for specific session
#Author: Aryan Khanna
#Version: Jan 9th, 2025

import requests
from bs4 import BeautifulSoup

#result_scraper method
#Description: This method receives the required url and scrapes the results to add it into a list in the format of
#[driver, team, lap_time, pos]
#
#PRE-CONDITIONS: .venv file should be present(donwload requests and beautifulSoup), the url provided should be an exisisting website
#
#POST-CONDITIONS: results are scraped and appended to result list to in the above mentioned format
#
#@params url, is str
#@return result, is a list
def result_scraper(url):

    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        print("Failed to retrieve the webpage.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select("tr")

    if "practice" or "starting" in url:
        pos_idx = 0
        driver_idx = 2
        team_idx = 3
        time_idx = 4

    if driver_idx == -1 or team_idx == -1 or time_idx == -1 or pos_idx == -1:
        print("Required columns not found in the table.")
        return []

    result = []

    for row in rows:
        cells = row.find_all("td")

        #Skip rows that don't have enough cells
        if len(cells) <= max(pos_idx, driver_idx, team_idx, time_idx):
            continue
        
        try:
            pos = cells[pos_idx].get_text(strip=True)
            driver = cells[driver_idx].get_text(strip=True)
            team = cells[team_idx].get_text(strip=True)
            lap_time = cells[time_idx].get_text(strip=True)
            result.append([driver, team, lap_time, pos])
        except IndexError:
            continue  #Skip problematic rows

    return result

#TODO: May have build another method to scrape points  
