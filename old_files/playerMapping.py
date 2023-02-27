#This is to map player names to their numbers

from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
# import playerStatsByCourse


#SOURCE: https://www.pgatour.com/players


def get_player_list():
    player_list = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    starting_url = "https://www.pgatour.com/players"
    origin_page = driver.get(starting_url)
    time.sleep(2)
    all_players = driver.find_elements(By.CSS_SELECTOR, "div span p a")
    for player in all_players:
        individual_player_dict = {}
        link = player.get_attribute('href')
        player_name = player.text
        player_number = link.split("/")[4]
        individual_player_dict["player_name"] = player_name
        individual_player_dict["player_number"] = player_number
        player_list.append(individual_player_dict)
    return player_list

def playerMap():
    allPlayers = [] #intialize list
    playerDict = {'backwards name': [], 'first name': [], 'last name': [], 'full name': []} #initialize dict
    for course in playerStatsByCourse.allCourses(): #call the scrape on all courses on the list
        tempList = course['player_name'].tolist()
        allPlayers.append(tempList)
    
    flatAllPlayers = flatten_list(allPlayers)

    removedDups = [] #need a list to remove dups
    for i in flatAllPlayers: #removing duplicates
         if i not in removedDups:
            removedDups.append(i)

    for player in removedDups: #adding full, fist, last name to dict & turning into df
        playerSplit = player.split(',')
        playerDict['backwards name'].append(playerSplit)
        playerDict['first name'].append(playerSplit[1][1:])
        playerDict['last name'].append(playerSplit[0])
        playerDict['full name'].append(f'{playerSplit[1][1:]} {playerSplit[0]}')
    player_df_course = pd.DataFrame.from_dict(playerDict)
    return player_df_course

def flatten_list(_2d_list): #flatten helper function
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

# dataGolfdf = playerMap()

# master = player_df.merge(dataGolfdf, how = 'right',on = 'full name') #merging with names
# master.drop('backwards name', inplace=True, axis=1)
# master = master.rename(columns={'first name_x': 'pga FN', 'last name_x': 'pga LN','first name_y': 'DG FN', 'last name_y': 'DG LN' })




