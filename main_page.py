import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

######################

@st.cache_resource # Cache data to improve performance
def load_data():
  df = pd.read_csv("./datasets/final_data.csv", encoding="utf-8")
  return df

data = load_data()

######################
# DATA IS FROM
# https://www.kaggle.com/datasets/etiennelq/french-employment-by-town/data
######################
# Add a sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Interactive overview", "Other page"])


######################
# Main page
######################
    
def Main_page():

    st.title("Salary insights and statistics in France")
    st.write("INSEE is the official french institute gathering data of many types around France\n.It can be demographic (Births, Deaths, Population Density…), Economic (Salary, Firms by activity / size…) and more. \n It can be a great help to observe and measure inequality in the French population.")


    # Add sliders for total_population and mean_salary
    min_population, max_population = st.slider("Select population range", min_value=min(data["total_population"]), max_value=max(data["total_population"]), value=(min(data["total_population"]), max(data["total_population"])))
    min_salary, max_salary = st.slider("Select mean salary range", min_value=min(data["mean_salary"]), max_value=max(data["mean_salary"]), value=(min(data["mean_salary"]), max(data["mean_salary"])))

    # Filter the data based on the slider values
    filtered_data = data[(data["total_population"] >= min_population) & (data["total_population"] <= max_population) & (data["mean_salary"] >= min_salary) & (data["mean_salary"] <= max_salary)]

    fig = px.scatter_mapbox(filtered_data, 
                            lat="latitude",
                            lon="longitude",
                            hover_name="Town", 
                            hover_data=["mean_salary", "total_firms"],
                            zoom=5,
                            )

    fig.update_layout(mapbox_style="carto-positron")

    st.subheader("FRANCE")
    st.plotly_chart(fig)

######################
#CALLING PAGES
######################
    
if page == "Interactive overview":
    Main_page()
elif page == "Other page":
    st.title("Other page")
    st.write("This is another page")

