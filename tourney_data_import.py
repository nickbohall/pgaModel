import pandas as pd

# This file is just for importing the csv data. The CSV data needs to be updated every year.
class DataImport:
    def __init__(self):
        path = "data/2015-2022 raw data tourneylevel condensed.csv"
        self.data = pd.read_csv(path)
        self.data["score"] = self.data.strokes - self.data.hole_par

    def get_data(self):
        return self.data
    def year_list(self):
        self.year_list = self.data.season.unique()

    def tourney_list(self):
        self.tourney_list = self.data["tournament name"].unique()

    def course_list(self):
        self.course_list = self.data.course.unique()