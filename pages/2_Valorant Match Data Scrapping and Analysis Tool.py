import streamlit as st
import pandas as pd

st.title("Valorant Match Data Processing and Prediction")

# Section 1: Introduction
st.header("Project Overview")
st.write(
    """
    This project involved automating the collection and processing of 150,000 Valorant match datasets 
    using BeautifulSoup and Requests libraries. The data was then filtered and cleaned with Pandas DataFrames, 
    ensuring 100% accuracy and narrowed down to 275 relevant datasets. To optimize data extraction, 
    a thread pool was used to enhance efficiency and minimize time for HTML requests. Additionally, 
    a scikit-learn model was built to predict game outcomes, achieving over 50% accuracy using only past match data.
    """
)

# Section 2: Data Display
st.header("Filtered and Processed Data")
st.subheader("First DataFrame")
st.write(
    '''
   Below is the filtered and cleaned DataFrame, showcasing processed Valorant match data specifically from games played in the Americas League. 
   This DataFrame includes each match twice, representing "team 1" and "team 2" separately. 
   Through web scraping, it captures every significant statistic from the match, including averages for players' ratings, kills, deaths, and more.
    '''
)
try:
    # Load the filtered data (assuming a CSV file or DataFrame object)
    data = pd.read_csv('/Users/tharun/Documents/Personal/Coding/API Prac/americas_vlr_games_stats_rolling.csv')  # Adjust the path accordingly
    data1 = data.iloc[:, 1:33]
    st.dataframe(data1)  
except Exception as e:
    st.error(f"Error loading data: {e}")

st.subheader("Second DataFrame")
st.write(
    '''
    Using the initial DataFrame, I created a second DataFrame with rolling averages of previous game statistics. 
    This approach allowed the machine learning model to use only past game data, preventing it from "cheating" 
    by including information from the game it is predicting.
    '''
)

try:
    data_part1 = data.iloc[:, 1:4]
    data_part2 = data.iloc[:, 32:]
    combined_data = pd.concat([data_part1,data_part2], axis=1)
    st.dataframe(combined_data)
except Exception as e:
    st.error(f"Error loading data: {e}")

# Section 3: Model Performance
st.header("Model Performance")
st.write(
    """
    The machine learning model built for predicting game outcomes achieved an accuracy of 58%. 
    
    """
)

# Example: If you have metrics, display them here
# st.write("Model Accuracy: 50%")

