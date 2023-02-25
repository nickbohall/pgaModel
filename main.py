import pandas as pd

from player_mapping import PlayerMap
from individual_stats import IndividualStats

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# players = Player_map()
# player_list = players.get_player_list()
# print(player_list)

individual_stats = IndividualStats()
scoring_average_df = individual_stats.get_scoring_table("https://www.pgatour.com/stats/detail/02675")
SG_total_df = individual_stats.get_scoring_table("https://www.pgatour.com/stats/detail/02675")
SG_OTT_df = individual_stats.get_scoring_table("https://www.pgatour.com/stats/detail/02567")
SG_ATG_df = individual_stats.get_scoring_table("https://www.pgatour.com/stats/detail/02569")
SG_TTG_df = individual_stats.get_scoring_table("https://www.pgatour.com/stats/detail/02674")
SG_APR_df = individual_stats.get_scoring_table("https://www.pgatour.com/stats/detail/02568")
SG_PUT_df = individual_stats.get_scoring_table("https://www.pgatour.com/stats/detail/02564")

print(SG_PUT_df)

