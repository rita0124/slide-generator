import plotly.express as px
import pandas as pd


class Chart():

    def __init__(self, df) -> None:
        self.dataframe = None
        self.fig = None

    def load_data(self, tasks):
        self.dataframe = pd.DataFrame(tasks)
        # self.dataframe = pd.DataFrame([
        #     dict(Task = "工作1", Start = '2023-09-13', End = '2023-10-25', Assigned = "Rita", Difficulty = 70),
        #     dict(Task = "工作5", Start = '2024-01-01', End = '2024-09-28', Assigned = "奴隸 C", Difficulty = 80)
        # ])

    def create_chart(self):
        self.fig = px.timeline(self.dataframe, x_start="Start", x_end="End", y="Task", color="Assigned")
        # Tasks from top to bottom
        self.fig.update_yaxes(autorange = "reversed") 
        # self.fig.show()

    def save_chart(self, filename):
        self.fig.write_image(filename)
