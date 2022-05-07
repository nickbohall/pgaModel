#Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

#Import data manipulation modules
import pandas as pd
import numpy as np

#other
from datetime import date

#other files
import playerMapping


year = date.today().year
start = 'https://www.pgatour.com/tournaments/' #just creating the links more efficiently, they all start with this
tourney = 'fortinet-championship' #This needs to be an array of tournaments to loop through
middle = '/past-results/jcr:content/mainParsys/pastresults.selectedYear.'
years = range(year-5, year+1)
end = '.004.html' #and end with this

url = f'{start}{tourney}{middle}{str(year)}{end}'
def tourneyStats(tourney):
    my_dict = {'player': {'year':[],'pos':[], 'score':[] }}
    my_df = pd.DataFrame()
    my_df['player number'] = playerMapping.player_df['player number']
    my_df['full name'] = playerMapping.player_df['full name']
    for year in years:
        url = f'{start}{tourney}{middle}{str(year)}{end}'
        r = requests.get(url).text
        t = pd.read_html(r)[0]
        t.reset_index()
        t.columns = [':'.join([i[0], i[1]]) if 'ROUNDS' in i else i[0] for i in t.columns]
        t.POS = t.POS.map(lambda x: x.split(' ')[-1])
        t['TO PAR'] = t['TO PAR'].map(lambda x: x.split(' ')[-1])
        round_columns = [i for i in t.columns if 'ROUNDS' in i]
        t[round_columns] = t[round_columns].applymap(lambda x: x.split(' ')[0])
        t = t.rename(columns={'PLAYER': 'full name', 'POS': f'{year} pos','TO PAR': f'{year} toPar'})
        df = t[['full name', f'{year} pos', f'{year} toPar']]
        df = df.replace('CUT', np.nan, regex=True)
        df = df.replace('T','', regex=True)
        df = df.replace('W/D','9000', regex=True)
        df = df.replace('E','0', regex=True)
        df = df.astype({f'{year} pos': 'Int64', f'{year} toPar': 'Int64'})
        my_df = my_df.merge(df, how='left', on= 'full name')
        
    my_df = my_df.dropna(thresh=3)
    my_df['posAvg'] = my_df[['2017 pos', '2018 pos', '2019 pos', '2020 pos', '2021 pos', '2022 pos']].mean(axis=1, skipna=True).round()
    my_df['scoreAvg'] = my_df[['2017 toPar', '2018 toPar', '2019 toPar', '2020 toPar', '2021 toPar', '2022 toPar']].mean(axis=1, skipna=True).round()
    return my_df.sort_values(by="scoreAvg", ascending = True)
    

print(tourneyStats('farmers-insurance-open'))