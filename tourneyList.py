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
    tourney = '-'.join(tourney.split()).lower()
    tourney = tourney.replace('\'', '') #get rid of ' for url
    tourneyListformatted.append(tourney)

#fixing one off's where url doesn't match the formula
tourneyListformatted = ['the-cj-cup' if item == 'the-cj-cup-@-summit' else item for item in tourneyListformatted]
tourneyListformatted = ['the-zozo-championship' if item == 'zozo-championship' else item for item in tourneyListformatted]
tourneyListformatted = ['bermuda-championship' if item == 'butterfield-bermuda-championship' else item for item in tourneyListformatted]
tourneyListformatted = ['at-t-pebble-beach-pro-am' if item == 'at&t-pebble-beach-pro-am' else item for item in tourneyListformatted]
tourneyListformatted = ['genesis-invitational' if item == 'the-genesis-invitational' else item for item in tourneyListformatted]
tourneyListformatted = ['wgc-dell-technologies-match-play' if item == 'world-golf-championships-dell-technologies-match-play' else item for item in tourneyListformatted]
tourneyListformatted = ['zurich-classic-of-new-orleans' if item == 'zurich-classic-of-new-orleans' else item for item in tourneyListformatted]
tourneyListformatted = ['at-t-byron-nelson' if item == 'at&t-byron-nelson' else item for item in tourneyListformatted]
tourneyListformatted = ['us-open' if item == 'u.s.-open' else item for item in tourneyListformatted]
tourneyListformatted = ['fedex-st-jude-championship' if item == 'fedex-st.-jude-championship' else item for item in tourneyListformatted]

tourneyListformatted.remove('ryder-cup')

print(tourneyListformatted)