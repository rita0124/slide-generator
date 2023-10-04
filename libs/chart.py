# -*- coding:utf-8 -*-
import plotly.express as px
import pandas as pd


class Chart():

    def __init__(self):
        self.dataframe = None
        self.fig = None

    def load_data(self, tasks):
        self.dataframe = pd.DataFrame(tasks)

    def create_chart(self):
        if len(self.dataframe) < 1:
            return
        self.fig = px.timeline(self.dataframe, x_start="Start", x_end="End", y="Task", color="Assigned")
        # Tasks from top to bottom
        self.fig.update_yaxes(autorange = "reversed") 

    def save_chart(self, filename):
        self.fig.write_image(filename)
