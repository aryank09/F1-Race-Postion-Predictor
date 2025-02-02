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

#build_driver_url method
#Description: This method receives the driver name and it accordingly produces a url for teh driver to get points 
#
#PRE-CONDITIONS: The driver name should be correctly spelt
#
#POST-CONDITIONS: url is built and returned
#
#@params driver_name, is str
#@return is a str
def build_driver_url(driver_name):
    
    base_url = "https://www.formula1.com/en/results/2024/drivers"

    # Driver codes and names (example data)
    drivers_data = {
        "MaxVerstappenVER": ("MAXVER01", "max-verstappen"),
        "LandoNorrisNOR": ("LANNOR01", "lando-norris"),
        "CharlesLeclercLEC": ("CHALEC01", "charles-leclerc"),
        "OscarPiastriPIA": ("OSCPIA01", "oscar-piastri"),
        "CarlosSainzSAI": ("CARSAI01", "carlos-sainz"),
        "GeorgeRussellRUS": ("GEORUS01", "george-russell"),
        "LewisHamiltonHAM": ("LEWHAM01", "lewis-hamilton"),
        "SergioPerezPER": ("SERPER01", "sergio-perez"),
        "FernandoAlonsoALO": ("FERALO01", "fernando-alonso"),
        "PierreGaslyGAS": ("PIEGAS01", "pierre-gasly"),
        "NicoHulkenbergHUL": ("NICHUL01", "nico-hulkenberg"),
        "YukiTsunodaTSU": ("YUKTSU01", "yuki-tsunoda"),
        "LanceStrollSTR": ("LANSTR01", "lance-stroll"),
        "EstebanOconOCO": ("ESTOCO01", "esteban-ocon"),
        "KevinMagnussenMAG": ("KEVMAG01", "kevin-magnussen"),
        "AlexanderAlbonALB": ("ALEALB01", "alexander-albon"),
        "DanielRicciardoRIC": ("DANRIC01", "daniel-ricciardo"),
        "OliverBearmanBEA": ("OLIBEA01", "oliver-bearman"),
        "FrancoColapintoCOL": ("FRACOL01", "franco-colapinto"),
        "ZhouGuanyuZHO": ("GUAZHO01", "zhou-guanyu"),
        "LiamLawsonLAW": ("LIALAW01", "liam-lawson"),
        "ValtteriBottasBOT": ("VALBOT01", "valtteri-bottas"),
        "LoganSargeantSAR": ("LOGSAR01", "logan-sargeant"),
        "JackDoohanDOO": ("JACDOO01", "jack-doohan"),
    }

    # Generate URLs for all drivers
    driver_code = drivers_data[driver_name][0]
    driver_url_name = drivers_data[driver_name][1]

    return f"{base_url}/{driver_code}/{driver_url_name}"

#build_constructor_url method
#Description: This method receives the constructor name and it accordingly produces a url for get constructor to get points 
#
#PRE-CONDITIONS: The constructor name should be correctly spelt
#
#POST-CONDITIONS: url is built and returned
#
#@params constructor_name, is str
#@return is a str
def build_constructor_url(constructor_name):
    constructors_url_map = {
    "McLaren Mercedes": "McLaren-Mercedes",
    "Ferrari": "Ferrari",
    "Red Bull Racing Honda RBPT": "Red-Bull-Racing-Honda-RBPT",
    "Mercedes": "Mercedes",
    "Aston Martin Aramco Mercedes": "Aston-Martin-Aramco-Mercedes",
    "Alpine Renault": "Alpine-Renault",
    "Haas Ferrari": "Haas-Ferrari",
    "RB Honda RBPT": "RB-Honda-RBPT",
    "Williams Mercedes": "Williams-Mercedes",
    "Kick Sauber Ferrari": "Kick-Sauber-Ferrari"
    }

    base_url = "https://www.formula1.com/en/results/2024/team/"

    return f"{base_url}{constructors_url_map[constructor_name]}"

#driver_points_scraper method
#
#Description: This method is resiponsible for scraping data to calculate driver points
#
#PRE-CONDITIONS: The race_weekend_name should be correctly spelt
#
#POST-CONDITIONS: drivers dictionary is returned which is a sum of the driver points upto that weekend
#
#@params race_weekend_name is a str
#@return drivers is a dictionary

def driver_points_scraper(race_weekend_name):
    drivers = {
        "MaxVerstappenVER": 0,
        "LandoNorrisNOR": 0,
        "CharlesLeclercLEC": 0,
        "OscarPiastriPIA": 0,
        "CarlosSainzSAI": 0,
        "GeorgeRussellRUS": 0,
        "LewisHamiltonHAM": 0,
        "SergioPerezPER": 0,
        "FernandoAlonsoALO": 0,
        "PierreGaslyGAS": 0,
        "NicoHulkenbergHUL": 0,
        "YukiTsunodaTSU": 0,
        "LanceStrollSTR": 0,
        "EstebanOconOCO": 0,
        "KevinMagnussenMAG": 0,
        "AlexanderAlbonALB": 0,
        "DanielRicciardoRIC": 0,
        "OliverBearmanBEA": 0,
        "FrancoColapintoCOL": 0,
        "ZhouGuanyuZHO": 0,
        "LiamLawsonLAW": 0,
        "ValtteriBottasBOT": 0,
        "LoganSargeantSAR": 0,
        "JackDoohanDOO": 0,
    }

    for driver_name in drivers:
        url = build_driver_url(driver_name)
        response = requests.get(url)
        if response.status_code != 200:
            print(response.status_code)
            print("Failed to retrieve the webpage.")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select("tr")

        grand_prix_indx = 0
        pts_indx = 4

        total_points = 0
        
        #writing to check if driver took part in the grand_prix
        races_participated = set()
        for row in rows:
            cells = row.find_all("td")
            if len(cells) <= max(grand_prix_indx, pts_indx):
                continue
            if (cells[grand_prix_indx].get_text(strip=True)).lower().replace(" ", "-") not in races_participated:
                races_participated.add((cells[grand_prix_indx].get_text(strip=True)).lower().replace(" ", "-"))

        for row in rows:
            cells = row.find_all("td")
            #Skip rows that don't have enough cells
            if len(cells) <= max(grand_prix_indx, pts_indx):
                continue
                
            if (race_weekend_name).lower().replace(" ", "-") not in races_participated:
                drivers[driver_name] = 0
                break

            try:  
                if (cells[grand_prix_indx].get_text(strip=True)).lower().replace(" ", "-") == (race_weekend_name).lower().replace(" ", "-"):
                    break
                total_points += int(cells[pts_indx].get_text(strip=True))
            except IndexError:
                continue  #Skip problematic rows
        
        drivers[driver_name] = total_points
    
    return drivers

#constructor_points_scraper method
#
#Description: This method is resiponsible for scraping data to calculate constructor points
#
#PRE-CONDITIONS: The race_weekend_name should be correctly spelt
#
#POST-CONDITIONS: constructors dictionary is returned which is a sum of the constructor points upto that weekend
#
#@params race_weekend_name is a str
#@return drivers is a dictionary

def constructors_points_scraper(race_weekend_name):
    constructors = {
    "McLaren Mercedes": 0,
    "Ferrari": 0,
    "Red Bull Racing Honda RBPT": 0,
    "Mercedes": 0,
    "Aston Martin Aramco Mercedes": 0,
    "Alpine Renault": 0,
    "Haas Ferrari": 0,
    "RB Honda RBPT": 0,
    "Williams Mercedes": 0,
    "Kick Sauber Ferrari": 0
    }

    for constructor_name in constructors:
        url = build_constructor_url(constructor_name)
        response = requests.get(url)
        if response.status_code != 200:
            print(response.status_code)
            print("Failed to retrieve the webpage.")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select("tr")

        grand_prix_indx = 0
        pts_indx = 2

        total_points = 0

        for row in rows:
            cells = row.find_all("td")
            #Skip rows that don't have enough cells
            if len(cells) <= max(grand_prix_indx, pts_indx):
                continue

            try:
                if (cells[grand_prix_indx].get_text(strip=True)).lower().replace(" ", "-") == (race_weekend_name).lower().replace(" ", "-"):
                    break
                total_points += int(cells[pts_indx].get_text(strip=True))
            except IndexError:
                continue  #Skip problematic rows
        
        constructors[constructor_name] = total_points
    
    return constructors

#build_race_result_url method
#Description: This method receives the constructor name and it accordingly produces a url for getting constructor to get points 
#
#PRE-CONDITIONS: The race_weekend name name should be correctly spelt
#
#POST-CONDITIONS: url is built and returned
#
#@params race_weekend_name, is str
#@return is a str

def build_race_result_url(race_weekend_name):
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
    "qatar": 1246,
    "mexico": 1248,
    "las-vegas": 1250,
    "abu-dhabi": 1252
    }
    race_name_key = race_weekend_name.lower().replace(" ", "-")
    race_id = race_id_mapping.get(race_name_key)
    return f"https://www.formula1.com/en/results/2024/races/{race_id}/{race_name_key}/race-result"

#race_result_position_scraper method
#
#Description: This method is resiponsible for scraping data to calculate race_result points
#
#PRE-CONDITIONS: The race_weekend_name should be correctly spelt
#
#POST-CONDITIONS: race_results dictionary is returned which is a sum of the race_result points upto that weekend
#
#@params race_weekend_name is a str
#@return drivers is a dictionary

def race_result_position_scraper(race_weekend_name):
    url = build_race_result_url(race_weekend_name)
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        print("Failed to retrieve the webpage.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select("tr")

    result = {}

    pos_idx = 0
    driver_idx = 2
    
    for row in rows:
        cells = row.find_all("td")

        # Skip rows that don't have enough cells
        if len(cells) <= max(pos_idx, driver_idx):
            continue
        
        try:
            pos = cells[pos_idx].get_text(strip=True)
            driver = cells[driver_idx].get_text(strip=True)
            result[driver] = pos  # Map driver name to position
        except IndexError:
            continue  # Skip problematic rows
        
    return result