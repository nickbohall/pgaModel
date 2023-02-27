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
        time.sleep(2)

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
        return starting_df
