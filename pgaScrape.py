#This file will be used for scraping https://www.pgatour.com/ for data

#Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#Import data manipulation modules
import pandas as pd
import numpy as np

#Dataviz
import matplotlib as mpl
import matplotlib.pyplot as plt

#other 
import re
import functools as ft

#other files
import playerMapping

start = 'https://www.pgatour.com/stats/stat.' #just creating the links more efficiently, they all start with this
end = '.html' #and end with this
url_dict = {'OTT': f'{start}02567{end}', 'TTG': f'{start}02674{end}', 'APTG': f'{start}02568{end}', 'ARTG': f'{start}02569{end}', 'PUTT': f'{start}02564{end}', 'TOT': f'{start}02675{end}', 'SCOR': f'{start}120{end}'}

def getStats(url, name):
    dict = {'Player Number': [], f'{name} average': [] } #Initialize dict to add to dF
    html_text = requests.get(url).text #goes to the url
    soup = BeautifulSoup(html_text, 'html.parser') #us BS to parse html
    table = soup.find('div', class_='details-table-wrap').find('table',class_='table-styled') #grabs the table
    players = table.find_all('tr', id = re.compile('playerStatsRow'))
    for player in players: 
        namesClass = player.find('td', class_='player-name')
        playerId = namesClass.find('a').get('href') #This just takes the first line: format - /players/player.08429.rodney-wilson.html
        playerNumber = playerId[slice(16,21)] #Parses just the number from ID & turns to int
        rankThisWeek = player.find('td', class_='').text.replace(' ','').strip()
        rankLastWeek = player.find('td', class_='hidden-print hidden-small hidden-medium').text.replace(' ','').strip()
        Rounds = player.find('td', class_='hidden-small hidden-medium').text.replace(' ','').strip()
        measuredRounds = player.find_all('td', class_='hidden-small hidden-medium')[-1].text.replace(' ','').strip()
        average = float(player.find('td', class_ = None).text.replace(' ','').strip())
        dict['Player Number'].append(playerNumber) #adding to dict
        dict[f'{name} average'].append(average) #adding to dict
    df = pd.DataFrame.from_dict(dict) #dict to df
    return df

OTT = getStats(url_dict['OTT'],"OTT")
TTG = getStats(url_dict['TTG'],"TTG")
APTG = getStats(url_dict['APTG'],"APTG")
ARTG = getStats(url_dict['ARTG'],"ARTG")
PUTT = getStats(url_dict['PUTT'],"PUTT")
SCOR = getStats(url_dict['SCOR'],"SCOR")
TOT = getStats(url_dict['TOT'],"TOT")

dfs = [OTT, TTG, APTG, ARTG, PUTT, SCOR, TOT]
df_merged = ft.reduce(lambda  left,right: pd.merge(left,right,on=['Player Number'], how='outer'), dfs)
master = playerMapping.player_df.merge(df_merged, how = 'right',on = 'Player Number') #merging with names
master['rank'] = master['TOT average'].rank(ascending=False).astype(int) #Creating rank column on TOT
master = master.sort_values(by=['rank']) #sorting by overall rank
print(master.head(20)
)










