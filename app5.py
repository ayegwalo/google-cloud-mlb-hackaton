import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

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

# Sidebar for Insights
st.sidebar.title('Data Insights')
language = st.selectbox('Select Language', ['English', 'Spanish', 'Japanese'])

# Default content in English
if language == 'English':
    st.sidebar.write("### Exit Velocity")
    st.sidebar.write("Exit velocity indicates how hard the ball is hit. Higher values generally result in longer home runs.")
    st.sidebar.write("### Launch Angle")
    st.sidebar.write("Launch angle is the trajectory of the ball after it leaves the bat. Ideal launch angles are typically between 20° and 30° for home runs.")

# Display content for other languages (only when selected)
elif language == 'Spanish':
    st.sidebar.write("### Velocidad de salida")
    st.sidebar.write("La velocidad de salida indica cuán fuerte se golpea la pelota.")
    st.sidebar.write("### Ángulo de lanzamiento")
    st.sidebar.write("El ángulo de lanzamiento es la trayectoria de la pelota después del impacto. Los ángulos ideales suelen estar entre 20° y 30° para los jonrones.")
    
elif language == 'Japanese':
    st.sidebar.write("### 打球速度")
    st.sidebar.write("打球速度は、ボールがどれだけ強く打たれたかを示します。")
    st.sidebar.write("### 打球角度")
    st.sidebar.write("打球角度は、バットからボールが飛び出す軌道です。理想的な角度は20°から30°の間です。")

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

# Add "Best of the Best" Section (Top Performances)
st.write("### Top Home Runs (Exit Velocity > 110 mph and Distance > 400 feet)")
top_home_runs = data[(data['ExitVelocity'] > 110) & (data['HitDistance'] > 400)].nlargest(10, 'ExitVelocity')
for idx, row in top_home_runs.iterrows():
    st.write(f"Player: {row['title']}, Exit Velocity: {row['ExitVelocity']} mph, Distance: {row['HitDistance']} feet")

# Interactive Player Stat Comparison (Side-by-Side)
if len(players) > 1:
    comparison_data = players_data.groupby('title').agg({
        'ExitVelocity': 'mean',
        'LaunchAngle': 'median',
        'HitDistance': 'mean'
    }).reset_index()

    st.write("### Player Stat Comparison")
    st.bar_chart(comparison_data.set_index('title'))

# Allow users to save favorite players
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if st.button('Save as Favorite'):
    for player in players:
        if player not in st.session_state.favorites:
            st.session_state.favorites.append(player)

st.write("### Your Favorite Players")
st.write(st.session_state.favorites)

# Basic Predictive Model for Exit Velocity
st.write("### Predict Exit Velocity for a Future Hit")
X = players_data[['LaunchAngle', 'HitDistance']]  # Features
y = players_data['ExitVelocity']  # Target
model = LinearRegression()
model.fit(X, y)

# Predict Exit Velocity for new data (example: Launch Angle = 22°, Hit Distance = 410 ft)
predicted_velocity = model.predict([[22, 410]])
st.write(f"Predicted Exit Velocity for future hit: {predicted_velocity[0]:.2f} mph")

# Allow the user to choose a specific hit based on distance
if players_data.shape[0] > 0:
    st.write("### Select a Hit Video")
    hit_choice = st.selectbox('Select Hit', players_data['HitDistance'].sort_values(ascending=False).head(10))

    # Get the video URL for the selected hit
    hit_video_url = players_data[players_data['HitDistance'] == hit_choice].iloc[0]['video']
    st.video(hit_video_url)
