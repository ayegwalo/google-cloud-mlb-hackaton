#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("google-cloud-mlb-hackathon")


# In[2]:


import sys

sys.version_info


# In[3]:


print(sys.version)


# In[4]:


import pandas as pd

# Correct raw URL of the CSV file
url = "https://raw.githubusercontent.com/MajorLeagueBaseball/google-cloud-mlb-hackathon/8ce90f707e19fb46496715b1bbbe2b702c9673b4/datasets/2016-mlb-homeruns.csv"

# Load the CSV file directly from the URL
data = pd.read_csv(url)

# Display the first few rows
data.head()


# In[5]:


print(data.info())


# In[6]:


# Fill missing numerical values with the median for better robustness
data['ExitVelocity'] = data['ExitVelocity'].fillna(data['ExitVelocity'].median())
data['HitDistance'] = data['HitDistance'].fillna(data['HitDistance'].median())
data['LaunchAngle'] = data['LaunchAngle'].fillna(data['LaunchAngle'].median())

# Optionally, fill missing titles with 'Unknown' (or you could drop these rows)
data['title'] = data['title'].fillna('Unknown')

# Check that there are no more missing values
print(data.isnull().sum())


# In[7]:


# Check for duplicates in play_id (which should be unique)
duplicates = data[data.duplicated(subset=['play_id'])]
print(f'Duplicates found: {duplicates.shape[0]}')


# In[8]:


# If duplicates exist, you can drop them
data = data.drop_duplicates(subset=['play_id'])


# In[9]:


print(data.tail())


# In[10]:


print(data.describe())


# In[11]:


print(data.isnull().sum)


# In[12]:


missing_values = data.isnull().sum()
print (missing_values)


# In[16]:


import streamlit as st
import matplotlib.pyplot as plt

# Streamlit header
st.title("Baseball Hit Analyzer")

# Filter by player (if the dataset contains player names)
player = st.selectbox('Select Player', data['title'].unique())

# Filter dataset by selected player
player_data = data[data['title'] == player]

# Plot Exit Velocity vs. Hit Distance
fig, ax = plt.subplots()
ax.scatter(player_data['ExitVelocity'], player_data['HitDistance'])
ax.set_xlabel('Exit Velocity (mph)')
ax.set_ylabel('Hit Distance (feet)')
ax.set_title(f'Exit Velocity vs Hit Distance for {player}')
st.pyplot(fig)

# Show a video of the selected hit (Assuming 'video' column contains video paths or URLs)
video_url = player_data.iloc[0]['video']
st.video(video_url)


# In[ ]:




