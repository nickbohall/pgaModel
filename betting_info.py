import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from player_mapping import PlayerMap

URL = "https://www.thelines.com/odds/golf/"


class BettingInfo:
    def __init__(self):
        options = Options()
        options.headless = True  # This is to not actually open the webpage
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.driver.get(URL)
        self.player_list = []
        self.odds_list = []
        self.averaged_odds_list = []

    # Helper function to turn a list into smaller lists of specified size. Found on Stack overflow
    def chunker(self, seq, size):
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def get_player_list(self):
        time.sleep(5)

        # Find all the players first and put them in a list

        players = self.driver.find_elements(By.CSS_SELECTOR, ".metabet-futures-board-entities div span")

        for player in players:
            player_clean = player.text.strip()
            self.player_list.append(player_clean)


    def get_odds_list(self):
        time.sleep(5)

        # Find the odds and put them in a list. Some cleaning and data manip had to be done

        odds = self.driver.find_elements(By.CSS_SELECTOR, ".metabet-futures-board-lines div")

        odds_clean_list = []
        for odd in odds:
            odd_clean = odd.text.strip().replace("+", "").replace(" ", "") # getting rid of the + symbol
            if odd_clean != "": # changing to int type
                odd_clean_int = int(odd_clean)
                odds_clean_list.append(odd_clean_int)
            else:
                odds_clean_list.append(np.nan)  # Replace blanks with Nan

        for clean in self.chunker(odds_clean_list, 6):  # using the chunker function
            self.odds_list.append(clean)


    def combine_to_df(self):
        # Calling helper functions above

        self.get_player_list()
        self.get_odds_list()

        # Combine the player list and odds list

        for i in range(
                len(self.player_list)):  # Loop through each players list and give them an average over the sportsbooks
            current_odds_list = self.odds_list[i]
            if np.isnan(current_odds_list).all():  # It won't average if they're all NaN
                average_odds = np.nan
            else:
                average_odds = round(np.nanmean(current_odds_list))
            self.averaged_odds_list.append(average_odds)

    def get_player_odds_df(self):

        # Calling functions to generate lists
        self.combine_to_df()

        return_dict = {"player_initial": self.player_list, "odds": self.averaged_odds_list}
        df = pd.DataFrame(return_dict)

        player_map_df = PlayerMap().first_initial_map() # bring in mapping to get the names right
        df = df.merge(player_map_df)
        df = df.drop(columns=['player_initial'])

        print("betting odds successfully gathered")

        return df