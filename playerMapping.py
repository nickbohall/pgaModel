#This is to map player names to their numbers

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re #Finds integers in strings
import courseMapping

playerDict = {'player number': [], 'first name': [], 'last name': [], 'full name': []} #intialize Dictionary
names = []
nameArray = []
numberArray = []

url = 'https://www.pgatour.com/players.html'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')
playerCard = soup.find_all('li', class_='player-card') #This is getting the general card of all
for player in playerCard: 
    playerId = player.find('a').get('href') #This just takes the first line: format - /players/player.08429.rodney-wilson.html
    playerNumber = playerId[slice(16,21)] #Parses just the number from ID & turns to int
    playerFirstName = player.find('span', class_='player-firstname').text #Gets first name as str
    playerLastName = player.find('span', class_='player-surname').text #Gets last name as str
    playerFullName = playerFirstName + ' ' + playerLastName #Combines full name
    playerDict['first name'].append(playerFirstName)
    playerDict['last name'].append(playerLastName)
    playerDict['player number'].append(playerNumber)   
    playerDict['full name'].append(f'{playerFirstName} {playerLastName}')

player_df = pd.DataFrame.from_dict(playerDict)

def playerMap():
    allPlayers = [] #intialize list
    playerDict = {'backwards name': [], 'first name': [], 'last name': [], 'full name': []} #initialize dict
    for course in courseMapping.allCourses(): #call the scrape on all courses on the list
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

dataGolfdf = playerMap()

master = player_df.merge(dataGolfdf, how = 'right',on = 'full name') #merging with names




