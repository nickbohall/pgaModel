#This is to map player names to their numbers

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re #Finds integers in strings

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
# print(player_df)




