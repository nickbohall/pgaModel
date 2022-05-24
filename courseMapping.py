#Import scraping modules
from bs4 import BeautifulSoup
import requests
import scrapy
import json

#Import data manipulation modules
import pandas as pd
import numpy as np

url = 'https://api.datagolf.ca/dg-api/v1/get_ch_data?callback=callback&course_num=ch_14&_=1653426856474'
html_text = requests.get(url).text #goes to the url
soup = BeautifulSoup(html_text, 'lxml') #us BS to parse html
body = soup.find('p').text.split('callback')[1][2:-3]
# ooi = json.loads(body)
split = body.split('}, ')[:-1]
course_dict = []
for ele in split:
    ele += '}'
    cdict = json.loads(ele)
    course_dict.append(cdict)
     
players = []
for player in course_dict:
    player_name = player['player_name']
    players.append(player_name)

print(players)