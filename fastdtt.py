# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:05:35 2023

@author: Home PC
"""

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")

st.title('Olympic History Dashboard')
st.subheader('Project Data Tools and Techniques - Sajjad Raza | Kulsoom Farhan | Shahrukh Raza | Muneeba Ahmed')


df1 = pd.read_csv("C:\\Users\\Home PC\\OneDrive\\Desktop\\DTT project\\athlete_events.csv")


df2 = pd.read_csv("C:\\Users\\Home PC\\OneDrive\\Desktop\\DTT project\\noc_regions.csv")

# merging the two table
df = df1.merge(df2 , how="left" , on='NOC')


df.info()

df.describe()

#check for null values
df.isna().sum()

df.head()

#dropping the notes feature as it has a lot of null values
df.drop( 'notes' , axis=1 , inplace= True )

df.head()

df['Age'].fillna(df['Age'].median(), inplace=True)
df["Height"].fillna(df["Height"].mean(), inplace=True)
df["Weight"].fillna(df["Weight"].mean(), inplace=True)

# Confirm that there are no more missing values in the data
print(df.isna().any())


# for region null values ,we will drop the rows which has null values  
df = df.dropna(axis=0, subset=['region'])
df.isna().any()

# for medal null values we recognize that the winners will have either a Gold, a Silver or a Bronze . so we can fill the null values with "No Medal"
df["Medal"].fillna("No Medal", inplace=True)
#check for null values again
df.isna().sum()

#to check the numerical columns is numerical( make sure that do not have string value)
for col in ['Age','Height','Weight']:
    df[col]=pd.to_numeric(df[col],errors='coerce')
    
# Now let us check if our dataset has any duplicate values
df.duplicated().sum()

df.drop_duplicates(keep='first',inplace=True)

# Create a dropdown widget to select the country

all_countries = sorted(df['region'].unique())
selected_country = st.selectbox('Select Your Country', all_countries)

# Filter the data based on the selected country
filtered_data = df[df["region"] == selected_country]

# Filter the data to only include gold, silver, and bronze medals
filtered_data_medals = filtered_data[filtered_data["Medal"].isin(['Gold', 'Silver', 'Bronze'])]

# Count the number of participations for the selected country
participations = filtered_data["region"].count()

# Count the number of gold medals for the selected country
gold_medals = filtered_data_medals[filtered_data_medals["Medal"] == "Gold"]["Medal"].count()

# Count the number of silver medals for the selected country
silver_medals = filtered_data_medals[filtered_data_medals["Medal"] == "Silver"]["Medal"].count()

# Count the number of bronze medals for the selected country
bronze_medals = filtered_data_medals[filtered_data_medals["Medal"] == "Bronze"]["Medal"].count()

# display the number of participations, gold medals, silver medals, and bronze medals using the `st.metrics()` function
col1, col2, col3, col4= st.columns(4)
col1.metric('Participations', participations)
col2.metric('Gold Medals', gold_medals)
col3.metric('Silver Medals', silver_medals)
col4.metric('Bronze Medals', bronze_medals)

st.set_option('deprecation.showPyplotGlobalUse', False)

with st.container():
    line, hbar, table = st.columns(3)

    line.header('Number of Medals over Years For Each Medal Type (G,S,B)')
    medal_counts = filtered_data_medals.groupby(['Year', 'Medal']).size().reset_index(name='No_of_medals')
    medal_data = medal_counts.sort_values('Year')
    if not medal_counts.empty:
        sns.lineplot(x='Year', y='No_of_medals', hue='Medal', data=medal_counts)
        line.pyplot()
    else:
        line.write("No medal data available for the selected country")

    hbar.header("Top 5 Athletes by Number of Medals Received")
    athlete_medal_count = filtered_data_medals.groupby(["Name"]).Medal.count().reset_index()
    athlete_medal_count = athlete_medal_count.sort_values("Medal", ascending=False).head(5)
    if not athlete_medal_count.empty:
        sns.barplot(x='Medal', y='Name', data=athlete_medal_count)
        hbar.pyplot()
    else:
        hbar.write("No athlete medal data available for the selected country")

    table.header("Top 5 Sports by Number of Medals Received")
    sport_medal_count = filtered_data_medals.groupby(["Sport"]).Medal.count().reset_index()
    sport_medal_count = sport_medal_count.sort_values("Medal", ascending=False).head(5)
    with table:
        if not sport_medal_count.empty:
            st.dataframe(sport_medal_count, height=200, width=400)
        else:
            table.write("No sport medal data available for the selected country")

with st.container():
    hist, pie, vbar = st.columns(3)

    hist.header("Number of Medals over Age Histogram Chart, 10 Years Bins")
    if not filtered_data_medals.empty:
        filtered_data_medals['Age'] = filtered_data_medals['Age'].astype(int)
        sns.histplot(x='Age', data=filtered_data_medals, bins=10)
        hist.pyplot()
    else:
        hist.write("No age data available for the selected country")

    pie.header("Pie Chart Summary by Number of Medals bifurcated by Gender")
    gender_medal_count = filtered_data_medals.groupby(["Sex"]).Medal.count().reset_index()
    if not gender_medal_count.empty:
        plt.pie(gender_medal_count["Medal"], labels=gender_medal_count["Sex"], autopct='%1.1f%%')
        pie.pyplot()
    else:
        pie.write("No gender-based medal data available for the selected country")

    vbar.header("Vertical Bar Chart by # of Medals Received in each Season")
    season_medal_count = filtered_data_medals.groupby(["Season"]).Medal.count().reset_index()
    if not season_medal_count.empty:
        sns.barplot(x='Season', y='Medal', data=season_medal_count)
        vbar.pyplot()
    else:
        vbar.write("No season-based medal data available for the selected country")


