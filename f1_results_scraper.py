import requests
from bs4 import BeautifulSoup

url_practice_1="https://www.formula1.com/en/results/2024/races/1252/abu-dhabi/practice/1"

response = requests.get(url_practice_1)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    print("Failed to retrieve the webpage.")
    exit()

#parsing and extracting data
driver_names = []
team_names = []
lap_times = []

table = soup.find('table', class_='resultsarchive-table')
if table:
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        cells = row.find_all('td')
        if cells:
            lap_time = cells[4].text.strip()  # Adjust index based on table
            driver_name = cells[2].text.strip()
            team_name = cells[3].text.strip()

            lap_times.append(lap_time)
            driver_names.append(driver_name)
            team_names.append(team_name)

# Step 3: Output or process the data
for lap, driver, team in zip(lap_times, driver_names, team_names):
    print(f"Lap Time: {lap}, Driver: {driver}, Team: {team}")
