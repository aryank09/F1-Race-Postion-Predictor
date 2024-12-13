import requests
from bs4 import BeautifulSoup

def result_scraper(url):
    #url="https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/1"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select("tr")
    else:
        print("Failed to retrieve the webpage.")
        exit()

    result = []

    for row in rows:
            #for all td tag elements
            cells = row.find_all("td")
            
            if len(cells) > 0:
                #getting the specific required data points 
                driver = cells[2].get_text(strip=True)
                team = cells[3].get_text(strip=True)
                lap_time = cells[4].get_text(strip=True)

                # Print the extracted data
                #print(f"Driver: {driver}, Team: {team}, Lap Time: {lap_time}")
                #inserting all the required data into an array
                temp = []
                temp.append(driver)
                temp.append(team)
                temp.append(lap_time)
                result.append(temp)
            else:
                print(f"Failed to fetch the webpage. Status code: {response.status_code}")
                return    
    return result
    
