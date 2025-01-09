import requests
from bs4 import BeautifulSoup

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

    # headers = []
    # for row in rows:
    #     th_cells = row.find_all("th")
    #     if th_cells:
    #         headers = [th.get_text(strip=True).upper() for th in th_cells]
    #         break  #Only process the first header row
    # print(headers)
    #Identifying column indices
    # driver_idx = headers.index("DRIVER") if "DRIVER" in headers else -1
    # team_idx = headers.index("CAR") if "CAR" in headers else -1
    # time_idx = headers.index("TIME") if "TIME" in headers else -1

    #print(driver_idx, team_idx, time_idx)

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

    
