import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# SOURCE: https://www.pgatour.com/players
class PlayerMap:
    def __init__(self):
        options = Options()
        options.headless = True  # This is to not actually open the webpage
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    def get_player_list(self):
        # setting up the final dict and temp lists
        player_dict = {}
        player_list = []
        player_number_list = []

        # getting the data and waiting for it to open
        starting_url = "https://www.pgatour.com/players"
        self.driver.get(starting_url)
        time.sleep(5)

        # run through all the players and get them in the right format for the dict
        all_players = self.driver.find_elements(By.CSS_SELECTOR, "div span p a")
        for player in all_players:
            link = player.get_attribute('href')
            player_name = player.text
            player_number = link.split("/")[4]
            player_list.append(player_name)
            player_number_list.append(player_number)

        # putting the lists in the dict to become a df
        player_dict['player'] = player_list
        player_dict['player_id'] = player_number_list
        starting_df = pd.DataFrame(player_dict)

        print("Player mapping list gathered")
        return starting_df

    # Function for getting the First initial and last name to match to the odds
    def first_initial_map(self):
        df = self.get_player_list()
        splitted = df['player'].str.split()
        first_name = splitted.str[0]
        first_init = first_name.str.split("")
        df['first_init'] = first_init.str[1] + "."
        df['last_name'] = df['player'].str.split(n=1).str[1]
        df['player_initial'] = df['first_init'].astype(str) + " " + df['last_name']
        df = df.drop(columns=['first_init', 'last_name', 'player_id'])

        return df

