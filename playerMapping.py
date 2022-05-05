#This is to map player names to their numbers

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re #Finds integers in strings

playerDict = {'First name': [], 'Last name': [], 'Player ID': []} #intialize Dictionary
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
    playerDict['First name'].append(playerFirstName)
    playerDict['Last name'].append(playerLastName)
    playerDict['Player ID'].append(playerNumber)   


player_df = pd.DataFrame.from_dict(playerDict)




