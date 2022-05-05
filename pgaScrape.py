#This file will be used for scraping https://www.pgatour.com/ for data

#Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

#Import data manipulation modules
import pandas as pd
import numpy as np

#Dataviz
import matplotlib as mpl
import matplotlib.pyplot as plt

#other
import requests

#other files
import playerMapping
import re

url = 'https://www.pgatour.com/stats/stat.02674.html'

def getStats(url, name):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.find('div', class_='details-table-wrap').find('table',class_='table-styled')
    players = table.find_all('tr', id = re.compile('playerStatsRow'))
    tds = table.find_all('tbody')
    for player in players: 
        namesClass = player.find('td', class_='player-name')
        playerId = namesClass.find('a').get('href') #This just takes the first line: format - /players/player.08429.rodney-wilson.html
        playerNumber = playerId[slice(16,21)] #Parses just the number from ID & turns to int
        rankThisWeek = player.find('td', class_='').text.replace(' ','').strip()
        rankLastWeek = player.find('td', class_='hidden-print hidden-small hidden-medium').text.replace(' ','').strip()
        Rounds = player.find('td', class_='hidden-small hidden-medium').text.replace(' ','').strip()
        measuredRounds = player.find_all('td', class_='hidden-small hidden-medium')[-1].text.replace(' ','').strip()
        average = player.find('td', class_ = None).text.replace(' ','').strip()
    # print(tds)
    

print(getStats(url))


