import pandas as pd

from player_mapping import PlayerMap
from individual_stats import IndividualStats
from tourney_finishes import TourneyFinishes
from betting_info import BettingInfo

current_tournament = "Masters Tournament"
current_course = "Augusta National Golf Club - Augusta, GA"

scoring_avg_url = "https://www.pgatour.com/stats/detail/120"
SG_total_url = "https://www.pgatour.com/stats/detail/02675"
SG_OTT_url = "https://www.pgatour.com/stats/detail/02567"
SG_ATG_url = "https://www.pgatour.com/stats/detail/02569"
SG_TTG_url = "https://www.pgatour.com/stats/detail/02674"
SG_APR_url = "https://www.pgatour.com/stats/detail/02568"
SG_PUT_url = "https://www.pgatour.com/stats/detail/02564"

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# ------------------------------------ PLAYER MAP ------------------------------------#

players = PlayerMap()
player_list = players.get_player_list()

#------------------------------------ INDIVIDUAL STATS ------------------------------------#

individual_stats = IndividualStats()
scoring_average_df = individual_stats.get_scoring_table_condensed(metric="scoring", url=scoring_avg_url)
SG_total_df = individual_stats.get_scoring_table_condensed(metric="SG total", url=SG_total_url)
SG_OTT_df = individual_stats.get_scoring_table_condensed(metric="SG OTT", url=SG_OTT_url)
SG_ATG_df = individual_stats.get_scoring_table_condensed(metric="SG ATG", url=SG_ATG_url)
SG_TTG_df = individual_stats.get_scoring_table_condensed(metric="SG TTG", url=SG_TTG_url)
SG_APR_df = individual_stats.get_scoring_table_condensed(metric="SG APR", url=SG_APR_url)
SG_PUT_df = individual_stats.get_scoring_table_condensed(metric="SG PUT", url=SG_PUT_url)

# ------------------------------------ TOURNEY STATS ------------------------------------#

tourney_finishes = TourneyFinishes()
tourney_scores = tourney_finishes.average_score_by_tourney(current_tournament)
course_scores = tourney_finishes.average_score_by_course(current_course)


# ------------------------------------ GET BETTING INFO ------------------------------------#

betting_info = BettingInfo()
current_tourney_odds = betting_info.get_player_odds_df()

# ------------------------------------ COMBINE DFS ------------------------------------#

merged_df = player_list\
    .merge(scoring_average_df, how="left")\
    .merge(SG_total_df, how="left")\
    .merge(SG_total_df, how="left")\
    .merge(SG_OTT_df, how="left")\
    .merge(SG_ATG_df, how="left")\
    .merge(SG_TTG_df, how="left")\
    .merge(SG_APR_df, how="left")\
    .merge(SG_PUT_df, how="left")\
    .merge(tourney_scores, how="left")\
    .merge(course_scores, how="left")\
    .merge(current_tourney_odds, how="left")\
    .merge(current_tourney_odds, how="left")

merged_df.to_csv("out.csv")

