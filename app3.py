import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import translate_v2 as translate
import requests
from io import BytesIO
from PIL import Image

# Streamlit header
st.title("Baseball Hit Analyzer")

# GitHub URL for dataset
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
language = st.selectbox('Select Language', ['English', 'Spanish', 'Japanese'], key="language_select")

# Function to translate text using Google Cloud Translate
def translate_text(text, target_language='es'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_lang=target_language)
    return result['translatedText']

# Show feedback message after language selection
if language == 'Spanish':
    st.write("Estás viendo la experiencia en Español.")
elif language == 'Japanese':
    st.write("日本語の体験を見ています。")
else:
    st.write("You're viewing the experience in English.")

# Streamlit controls for selecting player with a unique key
player = st.selectbox('Select Player', data['title'].unique(), key="select_player")

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

# Show player stats: average, min, max
player_avg_stats = player_data[['ExitVelocity', 'HitDistance', 'LaunchAngle']].agg(['mean', 'min', 'max'])
st.write(f"**{player} Stats**")
st.write(player_avg_stats)

# Optionally, display launch angle and batting average if available
if 'LaunchAngle' in player_data.columns:
    launch_angle_avg = player_data['LaunchAngle'].mean()
    st.write(f"Launch Angle Average: {launch_angle_avg:.2f}°")

# Let user select which metric to display
metric = st.radio("Select Metric to Compare", ['Exit Velocity', 'Hit Distance', 'Launch Angle'], key="metric_select")

# Plot based on selected metric
fig, ax = plt.subplots()
if metric == 'Exit Velocity':
    ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'], label=player, alpha=0.6, edgecolors="w", s=100)
    ax.set_xlabel('Exit Velocity (mph)')
    ax.set_ylabel('Hit Distance (feet)')
elif metric == 'Launch Angle':
    ax.scatter(player_data['LaunchAngle'], player_data['HitDistance'], label=player, alpha=0.6, edgecolors="w", s=100)
    ax.set_xlabel('Launch Angle (°)')
    ax.set_ylabel('Hit Distance (feet)')
else:
    ax.scatter(player_data['ExitVelocity'], player_data['LaunchAngle'], label=player, alpha=0.6, edgecolors="w", s=100)
ax.set_title(f'{metric} vs Hit Distance for {player}')
st.pyplot(fig)

# Plot histogram of Exit Velocity
st.subheader(f"Histogram of Exit Velocity for {player}")
fig, ax = plt.subplots()
ax.hist(player_data['ExitVelocity'], bins=30, color='skyblue', edgecolor='black')
ax.set_xlabel('Exit Velocity (mph)')
ax.set_ylabel('Frequency')
ax.set_title(f'Exit Velocity Distribution for {player}')
st.pyplot(fig)

# Correlation matrix for various stats
st.subheader(f"Correlation Matrix for {player}")
correlation_data = player_data[['ExitVelocity', 'HitDistance', 'LaunchAngle']]
correlation_matrix = correlation_data.corr()

# Plot the correlation matrix
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
ax.set_title(f'Correlation Matrix for {player}')
st.pyplot(fig)

# Show video of the selected hit
video_url = player_data.iloc[0]['video']

# Display the video using st.video() (since the URL is already a video)
st.video(video_url)

# Session state for favorite players
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Add player to favorites
def save_to_firestore(player_name):
    # Initialize Firestore client
    db = firestore.Client()
    doc_ref = db.collection('favorite_players').document(player_name)
    doc_ref.set({
        'name': player_name,
        'added_at': firestore.SERVER_TIMESTAMP
    })
    st.write(f"{player_name} added to your favorites!")

if st.button(f"Add {player} to Favorites", key="add_to_favorites"):
    st.session_state.favorites.append(player)
    save_to_firestore(player)  # Save to Firestore database

# Display favorite players
st.write("Your Favorite Players:")
st.write(st.session_state.favorites)

# Limit number of players to compare (e.g., max 5 players)
max_players = 5
players = st.multiselect('Select Players to Compare (Max 5)', data['title'].unique(), key="select_players_to_compare")

if len(players) > 1:
    if len(players) > max_players:
        st.warning(f"Please select up to {max_players} players only for comparison.")
    else:
        comparison_data = data[data['title'].isin(players)]
        chart_type = st.selectbox('Select Chart Type', ['Scatter Plot', 'Line Chart', 'Bar Chart'], key="chart_type")

        fig, ax = plt.subplots()
        if chart_type == 'Scatter Plot':
            colors = sns.color_palette("hsv", len(players))  # Get a color palette for each player
            for i, player in enumerate(players):
                player_data = comparison_data[comparison_data['title'] == player]
                ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'], label=player, color=colors[i], alpha=0.7, edgecolors="w", s=100)
            ax.set_xlabel('Exit Velocity (mph)')
            ax.set_ylabel('Hit Distance (feet)')
            ax.set_title(f'Exit Velocity vs Hit Distance Comparison')
            ax.legend()
        elif chart_type == 'Line Chart':
            for player in players:
                player_data = comparison_data[comparison_data['title'] == player]
                ax.plot(player_data['ExitVelocity'], player_data['HitDistance'], label=player)
            ax.set_xlabel('Exit Velocity (mph)')
            ax.set_ylabel('Hit Distance (feet)')
            ax.set_title(f'Exit Velocity vs Hit Distance Line Comparison')
            ax.legend()
        elif chart_type == 'Bar Chart':
            # Aggregate the data by player and take the mean of ExitVelocity and HitDistance
            comparison_data_mean = comparison_data.groupby('title')[['ExitVelocity', 'HitDistance']].mean().reset_index()

            # Shorten player names (for example: "Mike Trout" -> "M. Trout")
            comparison_data_mean['title_short'] = comparison_data_mean['title'].apply(lambda x: '. '.join([name[0] + '.' if i > 0 else name for i, name in enumerate(x.split())]))

            # Plot bar chart with shortened player names
            comparison_data_mean.plot(kind='bar', x='title_short', y=['ExitVelocity', 'HitDistance'], ax=ax)
            ax.set_ylabel('Average Value')
            ax.set_title(f'Bar Chart Comparison for {", ".join(players)}')

            # Rotate the x-axis labels for readability
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

        st.pyplot(fig)
