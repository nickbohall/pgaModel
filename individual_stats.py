import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class IndividualStats:
    def __init__(self):
        options = Options()
        options.headless = True  # This is to not actually open the webpage
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # This is a helper function to check the url and get the column headers to create the df
    def get_column_headers(self, url):
        url = url
        self.driver.get(url)
        time.sleep(2)

        data_table = self.driver.find_elements(By.CSS_SELECTOR, "thead.css-0 th")
        column_headers = [item.text for item in data_table]
        column_headers[1] = "TREND"
        return column_headers

    # This function takes a URL. It has to be in the same format as most of the stats tables.
    # It will return a DF with all the table information summarized. Call multiple times to get different stats
    def get_scoring_table(self, url):
        # getting the data and waiting for it to open
        column_headers = self.get_column_headers(url)

        self.driver.get(url)
        time.sleep(2)

        # finding the data table and iterating through
        data_table = self.driver.find_elements(By.CSS_SELECTOR, "tbody.css-0 tr")

        data_table_list = []
        for row in data_table:
            # Initialize individual Dict
            player_stats_dict = {}

            player_data = row.find_elements(By.CSS_SELECTOR, "td")
            player_data_clean = [item.text.replace("Expand Row", "").replace(",","").strip() for item in player_data]

            for i in range(len(column_headers)):
                item = player_data_clean[i]
                try:
                    item = float(item)
                except ValueError:
                    item = item
                player_stats_dict[column_headers[i]] = item

            #Add dict to list to be put in df
            data_table_list.append(player_stats_dict)

        df = pd.DataFrame(data_table_list)
        print("df successfully gathered")
        return df







