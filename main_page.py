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
page = st.sidebar.radio("Go to", ["Map overview", "Understanding Salary Inequalities", "Comparision of up to 3 cities","Definitions and Methodology"])

######################
# Main page
######################
    
def Main_page():

    data_copy = data.copy()
    data_copy = data_copy.rename(columns={"total_population": "Total Population", "Town":"Town", "longitude":"Longitude", "latitude": "Latitude", "mean_salary": "Mean net salary per hour (€)", "total_firms": "Total firms"})
    


    st.title("Salary insights and statistics in France")
    st.write("INSEE is the official french institute gathering data of many types around France\n.It can be demographic (Births, Deaths, Population Density…), Economic (Salary, Firms by activity / size…) and more. \n It can be a great help to observe and measure inequality in the French population.")

    st.write("In this visualization, we focus on displaying spatial information about the population, the mean salary and the number of firms in different towns in France.")

    st.subheader("Interactive map of France")
    st.write("Here we can see an interactive map of France. The map shows the towns in France with the mean salary per hour and the total number of firms. The map is interactive, so you can zoom in and out and hover over the towns to see more information about them. You can also filter the data based on the total population and the mean salary per hour using the sliders.")
    # Add sliders for total_population and mean_salary
    min_data_population = min(data["total_population"])
    max_data_population = max(data["total_population"])
    
    col1, col2 = st.columns(2)
    with col1:
        min_population = st.number_input(f"Minimum Population (above {min_data_population})", value=min_data_population, min_value=min_data_population, key="min_input")
    with col2:
        max_population = st.number_input(f"Maximum Population (below {max_data_population})", value=max_data_population, min_value=min_data_population, key="max_input")

    min_salary, max_salary = st.slider("Select mean salary range", min_value=min(data["mean_salary"]), max_value=max(data["mean_salary"]), value=(min(data["mean_salary"]), max(data["mean_salary"])))

    
    # Filter the data based on the slider values
    filtered_data = data_copy[(data_copy["Total Population"] >= min_population) & (data_copy["Total Population"] <= max_population) & (data_copy["Mean net salary per hour (€)"] >= min_salary) & (data_copy["Mean net salary per hour (€)"] <= max_salary)]
    

    fig = px.scatter_mapbox(filtered_data, 
                            lat="Latitude",
                            lon="Longitude",
                            hover_name="Town", 
                            hover_data=["Mean net salary per hour (€)", "Total firms"],
                            zoom=5,
                            )

    fig.update_layout(mapbox_style="carto-positron", height=950, width=710)

    st.plotly_chart(fig)

    def calculate_outlier_bounds(data_column):
        """Calculates IQR and outlier bounds for a data column."""
        q1 = data_column.quantile(0.25)
        q3 = data_column.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        return lower_bound, upper_bound

    def create_box_plot(data_column, show_outliers, use_log_axis=False):
        """Creates a box plot with optional outlier visibility and log axis."""
        box = px.box(data_copy, y=data_column, hover_name="Town")

        if not show_outliers:
            lower_bound, upper_bound = calculate_outlier_bounds(data_copy[data_column])
            box.update_traces(boxpoints=False)  # Hide box points
            box.update_layout(yaxis_range=[lower_bound, upper_bound])
            use_log_axis=False

        if use_log_axis:
            box.update_layout(yaxis_type="log")  # Set y-axis to log scale

        if not show_outliers and use_log_axis:
            # Adjust y-axis range for log scale when hiding outliers
            box.update_layout(yaxis_range=[max(lower_bound, 1), upper_bound])  # Set minimum to 1 for log

        return box

    # Create checkboxes for outlier visibility
    
    

    # Create and display box plots with outlier control
    st.subheader("Mean Salary by cities Distribution")

    show_salary_outliers = st.checkbox("Show outliers for Mean Salary", value=True)
    

    st.plotly_chart(create_box_plot("Mean net salary per hour (€)", show_salary_outliers))

    
    #salary_box = px.box(pd.DataFrame(data_copy[["Town","Mean net salary per hour (€)"]]), y="Mean net salary per hour (€)", hover_name = "Town")
    #population_box = px.box(pd.DataFrame(data_copy[["Town", "Total Population"]]), y="Total Population", hover_name = "Town")

    #st.subheader("Mean Salary by cities Distribution")
    #st.plotly_chart(salary_box)
    
    st.write("Here we can see the distribution of the mean salary per hour in different towns in France. The boxplot shows the median, the first and third quartiles, and the outliers. The outliers are the towns with the highest and lowest mean salary per hour. The boxplot is a great way to visualize the distribution of the data.")
    st.write("Interpretation : the wealthiest cities are generally cities located in Paris greater area. The salaries for these towns are so high compared to the rest of France that we cannot see the outliers for the lower salaries.")

    st.subheader("Total Population Distribution")
    
    show_population_outliers = st.checkbox("Show outliers for Total Population", value=True)
    
    if show_population_outliers:
        show_log = st.checkbox("Log scale for population", value=show_population_outliers)

    else:
        show_log = False

    st.plotly_chart(create_box_plot("Total Population", show_population_outliers,show_log))
    
    st.write("Here we can see the distribution of the total population in different towns in France. The boxplot shows the median, the first and third quartiles, and the outliers. The outliers are the towns with the highest and lowest total population. The boxplot is a great way to visualize the distribution of the data.")
    st.write("Interpretation : we can clearly see here the cities with a high population. Paris is an outlier with a very high population compared to the rest of France. The majority of the towns have a population of a few thousands of people.")
    
    


def Ineq_page():
    data_copy_2 = data.copy()
    data_copy_2 = data_copy_2.rename(columns={"nom_région": "Region", "total_population": "Total Population", "Town":"Town", "longitude":"Longitude", "latitude": "Latitude", "mean_salary": "Mean net salary per hour (€)", "total_firms": "Total firms"})
    
    st.title("Understanding Salary Inequalities in France")
    st.write("Here we will focus not only on the spatial repartion but also on the segmentation of the population by socio-professional categories, age groups and gender.")

    #Violin plot between male and female in france
    st.subheader("Violin plot of the mean salary per hour by gender")

    df_socio_professional = []

    for line in data_copy_2.iterrows():
        for gender in ["male", "female"]:
            for category in ["worker", "employee", "middle_manager", "executive"]:
                df_socio_professional.append({
                    "Town": line[1]["Town"],
                    "Region": line[1]["Region"],
                    "Departement": line[1]["Departement"],
                    "Mean Salary net per hour (€)": line[1][f"mean_{gender}_{category}_salary"],
                    "Category": category,
                    "Gender" : gender
                })

    df_socio_professional = pd.DataFrame(df_socio_professional)

    # Filter by region and department (assuming these are unique strings)
    region_options = ["All"] + df_socio_professional["Region"].unique().tolist()  # Add "All" option
    region_filter= st.selectbox("Select Region Name", options=region_options, index=0)
    departement_options = ["All"] + df_socio_professional["Departement"].unique().tolist()  # Add "All" option
    departement_filter= st.selectbox("Select Departement", options=departement_options, index=0)
    
    category_options = ["All"] + df_socio_professional["Category"].unique().tolist()  # Add "All" option
    category_filter = st.selectbox("Select Category", options=category_options, index=0)

    # Apply filtering based on selection
    if region_filter == "All":
        filtered_df_2 = df_socio_professional.copy()  # Show all rows if "All" is selected for region
    else:
        filtered_df_2 = df_socio_professional[df_socio_professional["Region"] == region_filter]

    if departement_filter == "All":
        filtered_df_2 = filtered_df_2.copy()  # Apply department filter only if region filter wasn't "All"
    else:
        filtered_df_2 = filtered_df_2[filtered_df_2["Departement"] == departement_filter]

    if category_filter == "All":
        filtered_df_2 = filtered_df_2.copy()
    else:
        filtered_df_2 = filtered_df_2[filtered_df_2["Category"] == category_filter]
    
    boxes_1 = st.checkbox("Show box plot on top of violin plot", value=True)

    # Use px.violin with color to differentiate genders
    fig_csp = px.violin(filtered_df_2, 
                    y="Mean Salary net per hour (€)", 
                    color="Gender", 
                    box=boxes_1, 
                    hover_name="Town", 
                    hover_data=filtered_df_2.columns)
    
    st.plotly_chart(fig_csp)
    
    
    st.write("Here, we can see the distribution of the mean salary per hour in different towns across France. The violin plot shows the distribution of the mean hourly salary in EUR.")
    st.write("Interpretation: We can see that the mean salary is generally higher for men than for women.")
    st.write("Try exploring other departments and socio-professional categories. You will notice that we cannot generalize the situation for every region in France. There are many inequalities, and each region faces its own difficulties.")


    ###
    # AGE
    ###
    st.subheader("Violin plot of the mean salary per age")

    df_age = []

    for line in data_copy_2.iterrows():
        for age in ["young", "medium", "old"]:
            df_age.append({
                    "Town": line[1]["Town"],
                    "Region": line[1]["Region"],
                    "Departement": line[1]["Departement"],
                    "Mean Salary net per hour (€)": line[1][f"mean_{age}_age_salary"], #mean_young_age_salary
                    "Age": age,
                })

    df_age = pd.DataFrame(df_age)
        
    # Filter by region and department (assuming these are unique strings)
    region_options_2 = ["All"] + df_age["Region"].unique().tolist()  # Add "All" option
    region_filter_2= st.selectbox("Select Region Name :", options=region_options_2, index=0)
    departement_options_2 = ["All"] + df_age["Departement"].unique().tolist()  # Add "All" option
    departement_filter_2= st.selectbox("Select Departement :", options=departement_options_2, index=0)
    
    # Apply filtering based on selection
    if region_filter_2 == "All":
        filtered_df_3 = df_age.copy()  # Show all rows if "All" is selected for region
    else:
        filtered_df_3 = df_age[df_age["Region"] == region_filter_2]

    if departement_filter_2 == "All":
        filtered_df_3 = filtered_df_3.copy()  # Apply department filter only if region filter wasn't "All"
    else:
        filtered_df_3 = filtered_df_3[filtered_df_3["Departement"] == departement_filter_2]

    boxes_2 = st.checkbox("Show box plot on top of violin plot ", value=True)

    # Create a box plot with age groups on the x-axis and salary on the y-axis, colored by town
    fig_age = px.violin(filtered_df_3, 
                y="Mean Salary net per hour (€)", 
                color="Age", 
                box = boxes_2,
                title="Mean Salary per Hour by Age Group and Town",
                hover_name="Town",
                hover_data=filtered_df_3.columns
                )

    st.plotly_chart(fig_age)

    st.write("This box plot shows the distribution of mean hourly salary (€) across different age groups in French towns. We can observe a general trend of higher salaries for older age groups.")
    st.write("Interpretation: The plot reveals age-based salary inequalities within each region and across France as a whole. For a more detailed view, try selecting the 'Île-de-France' region to see how these inequalities manifest within that specific area.")
    # Optional customizations (adjust as needed)
    

def City_comparison():
    st.title("Comparision of up to 3 cities")
    st.write("Here we will compare up to 3 cities in France based on the mean salary per hour. You can select the segmentation you want between the socio-professional category, the gender and the age")
    st.write('If you want to compare only 2 cities, select "None" for the third city.')

    data_copy_3 = data.copy()

    # Get a unique list of town names
    town_options = ['None'] + data_copy_3['Town'].unique().tolist()
    #Default towns : Paris, Marseille, Lyon
    paris_index = [i for i, town in enumerate(town_options) if town == "Paris"][0]
    grenoble_index = [i for i, town in enumerate(town_options) if town == "Grenoble"][0]
    # Add an "All" option for filtering
    town_filter_1 = st.selectbox("Select First Town:", options=town_options, index=paris_index) 
    town_filter_2 = st.selectbox("Select Second Town:", options=town_options, index=grenoble_index) 
    town_filter_3 = st.selectbox("Select Third Town:", options=town_options, index=0) 

    filtered_df = data_copy_3[data_copy_3['Town'].isin([town_filter_1, town_filter_2, town_filter_3])]

    # Create a bar chart to compare the mean salary per hour by gender of the two selected towns
    st.subheader("Comparing caracteristics of those two towns:")
    possible_options = ["Socio-professional Category", "Age","Gender"]
    filter= st.selectbox("Select segmentation :", options=possible_options, index=0)

    if filter == "Gender":
        df_gender = []
        for line in filtered_df.iterrows():
            for gender in ["male", "female"]:
                df_gender.append({
                        "Town": line[1]["Town"],
                        "Region": line[1]["nom_région"],
                        "Departement": line[1]["Departement"],
                        "Gender" :  gender,
                        "Mean Salary net per hour (€)": line[1][f"mean_{gender}_salary"], 
                    })

        df_gender = pd.DataFrame(df_gender)

        male_df = df_gender[df_gender["Gender"]== "male"]
        trace_1 = go.Bar(x = male_df["Town"], y=male_df['Mean Salary net per hour (€)'])
        trace_1.name = "Male"

        female_df = df_gender[df_gender["Gender"]== "female"]
        trace_2 = go.Bar(x = female_df["Town"], y=female_df['Mean Salary net per hour (€)'])
        trace_2.name = "Female"

        # Combine traces and create the layout
        fig = go.Figure(data=[trace_1, trace_2])

        # Update layout with axis titles
        fig.update_layout(
            xaxis_title="Town",  # Title for the x-axis
            yaxis_title="Mean Net Salary (€)"  # Title for the y-axis
        )

    if filter == "Age":
        df_age = []
        for line in filtered_df.iterrows():
            for age in ["young", "medium", 'old']:
                df_age.append({
                        "Town": line[1]["Town"],
                        "Region": line[1]["nom_région"],
                        "Departement": line[1]["Departement"],
                        "Age" :  age,
                        "Mean Salary net per hour (€)": line[1][f"mean_{age}_age_salary"], 
                    })

        df_age = pd.DataFrame(df_age)

        young_df = df_age[df_age["Age"]== "young"]
        trace_1 = go.Bar(x = young_df["Town"], y=young_df['Mean Salary net per hour (€)'])
        trace_1.name = "Young"

        medium_df = df_age[df_age["Age"]== "medium"]
        trace_2 = go.Bar(x = medium_df["Town"], y=medium_df['Mean Salary net per hour (€)'])
        trace_2.name = "Medium"

        old_df = df_age[df_age["Age"]== "old"]
        trace_3 = go.Bar(x = old_df["Town"], y=old_df['Mean Salary net per hour (€)'])
        trace_3.name = "Old"

        # Combine traces and create the layout
        fig = go.Figure(data=[trace_1, trace_2, trace_3])
        # Update layout with axis titles
        fig.update_layout(
            xaxis_title="Town",  # Title for the x-axis
            yaxis_title="Mean Net Salary (€)"  # Title for the y-axis
        )

    if filter == "Socio-professional Category":
        df_socio_professional = []
        for line in filtered_df.iterrows():
            for category in ["worker", "employee", "middle_manager", "executive"]:
                df_socio_professional.append({
                        "Town": line[1]["Town"],
                        "Region": line[1]["nom_région"],
                        "Departement": line[1]["Departement"],
                        "Category" :  category,
                        "Mean Salary net per hour (€)": line[1][f"mean_{category}_salary"], 
                    })
        
        df_socio_professional = pd.DataFrame(df_socio_professional)

        executive_df = df_socio_professional[df_socio_professional["Category"]== "executive"]
        trace_1 = go.Bar(x = executive_df["Town"], y=executive_df['Mean Salary net per hour (€)'])
        trace_1.name = "Executive"

        middle_manager = df_socio_professional[df_socio_professional["Category"]== "middle_manager"]
        trace_2 = go.Bar(x = middle_manager["Town"], y=middle_manager['Mean Salary net per hour (€)'])
        trace_2.name = "Middle Manager"

        employee_df = df_socio_professional[df_socio_professional["Category"]== "employee"]
        trace_3 = go.Bar(x = employee_df["Town"], y=employee_df['Mean Salary net per hour (€)'])
        trace_3.name = "Employee"

        worker_df = df_socio_professional[df_socio_professional["Category"]== "worker"]
        trace_4 = go.Bar(x = worker_df["Town"], y=worker_df['Mean Salary net per hour (€)'])
        trace_4.name = "Worker"

        # Combine traces and create the layout
        fig = go.Figure(data=[trace_1, trace_2, trace_3,trace_4])
        # Update layout with axis titles
        fig.update_layout(
            xaxis_title="Town",  # Title for the x-axis
            yaxis_title="Mean Net Salary (€)"  # Title for the y-axis
        )
    
    st.plotly_chart(fig)
    st.write('This bar chart shows the mean salary per hour in EUR for the selected towns. The chart is segmented by the selected category. The chart allows you to compare the mean salary per hour for different towns based on the selected category.')
    st.write('Interpretation: The chart reveals the mean salary per hour for the selected towns based on the selected category. You can see the differences in mean salary per hour for different towns based on the selected category.')
    st.write('Try exploring by comparing Paris and Marseille, the two most populated cities. You can see that Marseille has a lower mean salary per hour compared to Paris. This is due to the difference in the cost of living between the two cities. Paris is known for its high cost of living, which is reflected in the higher mean salary per hour compared to Marseille.')


    st.subheader("Locate the towns on the map")
    df_map = filtered_df[["Town", "latitude", "longitude", "mean_salary"]]
    df_map.columns = ["Town", "Latitude", "Longitude", "Mean net salary per hour (€)"]
    sizes = [3]*df_map.shape[0]
    # Create a scatter plot to show the selected towns on the map
    fig_2 = px.scatter_mapbox(df_map, 
                            lat="Latitude",
                            lon="Longitude",
                            hover_name="Town", 
                            hover_data=["Mean net salary per hour (€)"],
                            zoom=5,
                            size = sizes
                            )

    fig_2.update_layout(mapbox_style="carto-positron", height=950, width=710)

    st.plotly_chart(fig_2)
    
def Definitions():
    st.title("Definitions and Methodology")
    st.subheader("Methodology")
    st.write("The data used in this visualization was obtained from this Kaggle dataset : https://www.kaggle.com/datasets/etiennelq/french-employment-by-town/data")
    st.write("The dataset contains information about the town, salaries and population in France in multiple files. During the preprocessing, we merged those files and renamed the columns to make the data readable.")
    st.write("For example, the column 'SNHMFC14', which represents the mean net salary per hour for feminin executive according to the dataset, was renamed mean_female_executive_salary.")
    st.write("We took the preprocessing on this link : https://www.kaggle.com/code/dirkxie/data-preparation and we modified it to obtain more precise information for each town about the region, the departement, the population.")
    st.write("At the end of the preprocessing, we get a single dataset with one line per town and information for each segmentation of the population.")
    st.write("Original datasets are heavy so we put only the preprocessed data in the github repository. The original data can be found in the Kaggle dataset.")

    st.write("Our Github link : https://github.com/theveneth/DV_project ")


    st.subheader("Definitions")

    st.write("AGES : ")
    st.write("- Young : 18-25 years old")
    st.write("- Medium : 26-50 years old")
    st.write("- Old : 51 years old and above")

######################
#CALLING PAGES
######################
    
if page == "Map overview":
    Main_page()
elif page == "Understanding Salary Inequalities":
    Ineq_page()
elif page == "Comparision of up to 3 cities":
    City_comparison()
elif page == "Definitions and Methodology":
    Definitions()

