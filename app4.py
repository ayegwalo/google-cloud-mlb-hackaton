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
# Sidebar for Insights
st.sidebar.title('Data Insights')
st.sidebar.write('### Exit Velocity')
st.sidebar.write('Exit velocity indicates how hard the ball is hit. Higher values generally result in longer home runs.')
st.sidebar.write('### Launch Angle')
st.sidebar.write('Launch angle is the trajectory of the ball off the bat. Ideal launch angles are typically between 20° and 30° for home runs.')

# Allow the user to select multiple players
players = st.multiselect('Select Players', data['title'].unique())

# Filter dataset for selected players
players_data = data[data['title'].isin(players)]

# Plot Exit Velocity vs Hit Distance for selected players
fig, ax = plt.subplots()

# Add scatter plot for each player
for player in players:
    player_data = players_data[players_data['title'] == player]
    ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'], label=player)

ax.set_xlabel('Exit Velocity (mph)')
ax.set_ylabel('Hit Distance (feet)')
ax.set_title(f'Exit Velocity vs Hit Distance for Selected Players')
ax.legend()
st.pyplot(fig)

# Statistical summaries
if players:
    for player in players:
        player_data = players_data[players_data['title'] == player]
        
        # Calculate statistics
        avg_exit_velocity = player_data['ExitVelocity'].mean()
        median_launch_angle = player_data['LaunchAngle'].median()
        home_run_count = player_data[player_data['HitDistance'] > 400].shape[0]  # Assuming 400 feet is a home run distance
        
        # Display player stats
        st.write(f"### {player}'s Stats")
        st.write(f"Average Exit Velocity: {avg_exit_velocity:.2f} mph")
        st.write(f"Median Launch Angle: {median_launch_angle:.2f}°")
        st.write(f"Home Runs (Distance > 400 feet): {home_run_count}")

# Allow the user to choose a specific hit based on distance
if players_data.shape[0] > 0:
    st.write("### Select a Hit Video")
    hit_choice = st.selectbox('Select Hit', players_data['HitDistance'].sort_values(ascending=False).head(10))

    # Get the video URL for the selected hit
    hit_video_url = players_data[players_data['HitDistance'] == hit_choice].iloc[0]['video']
    st.video(hit_video_url)
