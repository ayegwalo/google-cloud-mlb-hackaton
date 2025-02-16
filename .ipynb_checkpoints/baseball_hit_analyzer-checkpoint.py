
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
data = pd.read_csv('path_to_your_data.csv')  # Make sure the path is correct

# Handle missing data
data['ExitVelocity'] = data['ExitVelocity'].fillna(data['ExitVelocity'].median())
data['HitDistance'] = data['HitDistance'].fillna(data['HitDistance'].median())
data['LaunchAngle'] = data['LaunchAngle'].fillna(data['LaunchAngle'].median())
data['title'] = data['title'].fillna('Unknown')

# Optional: Create a Hit Score
data['HitScore'] = data['ExitVelocity'] * data['HitDistance'] * (90 - abs(data['LaunchAngle'] - 25)) / 10000

# Streamlit UI Components
st.title("Baseball Hit Analyzer")
st.subheader("Explore Exit Velocity, Hit Distance, Launch Angle, and more!")

# Player selection
player = st.selectbox('Select Player/Title', data['title'].unique())
player_data = data[data['title'] == player]

# Scatter plot for Exit Velocity vs Hit Distance
fig, ax = plt.subplots()
ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'])
ax.set_xlabel('Exit Velocity (mph)')
ax.set_ylabel('Hit Distance (feet)')
ax.set_title(f'Exit Velocity vs Hit Distance for {player}')
st.pyplot(fig)

# Display video
video_url = player_data.iloc[0]['video']
st.video(video_url)
