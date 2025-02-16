import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from google.cloud import translate_v2 as translate
import requests
from PIL import Image
from io import BytesIO

# Streamlit header
st.title("Baseball Hit Analyzer")

# github url link
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

# Language selection
language = st.selectbox('Select Language', ['English', 'Spanish', 'Japanese'])

# Function to translate text using Google Cloud Translate
def translate_text(text, target_language='es'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_lang=target_language)
    return result['translatedText']

# Streamlit controls for selecting player
player = st.selectbox('Select Player', data['title'].unique())

# Set the title based on language
if language == 'Spanish':
    title = translate_text("Exit Velocity vs Hit Distance for", target_language='es')
    st.title(f"{title} {player}")
elif language == 'Japanese':
    title = translate_text("Exit Velocity vs Hit Distance for", target_language='ja')
    st.title(f"{title} {player}")
else:
    st.title(f"Exit Velocity vs Hit Distance for {player}")

# Filter dataset by selected player
player_data = data[data['title'] == player]

# Plot Exit Velocity vs Hit Distance
fig, ax = plt.subplots()
ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'])
ax.set_xlabel('Exit Velocity (mph)')
ax.set_ylabel('Hit Distance (feet)')
ax.set_title(f'Exit Velocity vs Hit Distance for {player}')
st.pyplot(fig)

# Show video of the selected hit
video_url = player_data.iloc[0]['video']

# Display the video using st.video() (since the URL is already a video)
st.video(video_url)

# Add a button to save the player to favorites (session state)
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Add player to favorites
if st.button(f"Add {player} to Favorites"):
    st.session_state.favorites.append(player)

# Display favorite players
st.write("Your Favorite Players:")
st.write(st.session_state.favorites)

# Allow user to compare stats for multiple players
players = st.multiselect('Select Players to Compare', data['title'].unique())

if len(players) > 1:
    comparison_data = data[data['title'].isin(players)]
    fig, ax = plt.subplots()
    for player in players:
        player_data = comparison_data[comparison_data['title'] == player]
        ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'], label=player)
    ax.set_xlabel('Exit Velocity (mph)')
    ax.set_ylabel('Hit Distance (feet)')
    ax.set_title(f'Exit Velocity vs Hit Distance Comparison')
    ax.legend()
    st.pyplot(fig)
