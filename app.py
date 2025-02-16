
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Streamlit header
st.title("Baseball Hit Analyzer")

# Correct raw URL of the CSV file
url = "https://raw.githubusercontent.com/MajorLeagueBaseball/google-cloud-mlb-hackathon/8ce90f707e19fb46496715b1bbbe2b702c9673b4/datasets/2016-mlb-homeruns.csv"

# Load the CSV file directly from the URL
data = pd.read_csv(url)

# Handle missing values
data['ExitVelocity'] = data['ExitVelocity'].fillna(data['ExitVelocity'].median())
data['HitDistance'] = data['HitDistance'].fillna(data['HitDistance'].median())
data['LaunchAngle'] = data['LaunchAngle'].fillna(data['LaunchAngle'].median())
data['title'] = data['title'].fillna('Unknown')

# Check for duplicates
data = data.drop_duplicates(subset=['play_id'])

# Streamlit controls
player = st.selectbox('Select Player', data['title'].unique())

# Filter dataset by selected player
player_data = data[data['title'] == player]

# Plot Exit Velocity vs Hit Distance
fig, ax = plt.subplots()
ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'])
ax.set_xlabel('Exit Velocity (mph)')
ax.set_ylabel('Hit Distance (feet)')
ax.set_title(f'Exit Velocity vs Hit Distance for {player}')
st.pyplot(fig)

# Show a video of the selected hit
video_url = player_data.iloc[0]['video']
st.video(video_url)
