import pandas as pd
import plotly.express as px


def load_data():
  df = pd.read_csv("./datasets/final_data.csv", encoding="utf-8")
  return df

data = load_data()


fig = px.scatter_mapbox(data, 
                        lat="latitude",
                        lon="longitude",
                        hover_name="Town", 
                        hover_data=["mean_salary", "total_firms"],
                        zoom=5,
                        )

fig.update_layout(mapbox_style="carto-positron")

fig.show()