#Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#Import data manipulation modules
import pandas as pd
import numpy as np
import re

courseList = []
tourneyListformatted = []

url = 'https://api.datagolf.ca/dg-api/v1/get_ch_data?callback=callback&course_num=ch_14&_=1653426856474'
r = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser') #us BS to parse html



# tourneys = soup.find('body').find('div', class_='wrapper').find('div', class_='container-fluid').find('div', class_='table-container')
# print(tourneys)
# for tourney in tourneys:
#     tourn = tourney.find('br').text.replace(' ', '').strip().split(',')[0]
#     courseList.append(tourn)
# print(courseList)
# for tourney in tourneyList: 
#     tourney = '-'.join(tourney.split()).lower()
#     tourney = tourney.replace('\'', '') #get rid of ' for url
#     tourneyListformatted.append(tourney)