#Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#Import data manipulation modules
import pandas as pd
import numpy as np
import re

tourneyList = []
tourneyListformatted = []

url = 'https://www.pgatour.com/tournaments/schedule.html'
html_text = requests.get(url).text #goes to the url
soup = BeautifulSoup(html_text, 'html.parser') #us BS to parse html
tourneys = soup.find('div', class_='wrap').find_all('div', class_='tournament-text')
for tourney in tourneys:
    try: tourn = tourney.find('a').text
    except: tourn = tourney.find('span').text
    tourneyList.append(tourn)

for tourney in tourneyList: 
    tourney = '-'.join(tourney.split())
    tourneyListformatted.append(tourney)

print(tourneyListformatted)