#Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#Import data manipulation modules
import pandas as pd
import numpy as np

start = 'https://www.pgatour.com/players/player.' #just creating the links more efficiently, they all start with this
end = '.html' #and end with this
url = f'{start}46970.jon-rahm{end}'

html_text = requests.get(url).text #goes to the url
soup = BeautifulSoup(html_text, 'html.parser') #us BS to parse html
test = soup.find('body').find('div', class_='wrap').find('div',class_='container').find('div', class_='clearfix module-player-navigation').find('div', class_='tabbable')\
.find('div', class_='tab-content tab-content-players-overview').find('div', class_='player-performance performance').find('section').find('div', class_='tabbable player-section-performance')\
.find('div', class_='tab-content').find('div', id='performanceMajors').find_all()

test3 = soup.find('div', class_='player-performance performance')



majors_table = soup.find('div', class_='player-performance performance')#.find('section', id='performance').find('div', class_='tabbable player-section-performance').find('div', class_='tab-content') \
                #.find('div', id= 'performanceMajors').find('script')
print (test3)
print(url)