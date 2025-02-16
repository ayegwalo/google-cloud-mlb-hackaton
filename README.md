# google-cloud-mlb-hackaton
# ⚾ Baseball Hit Analyzer

## Overview

The **Baseball Hit Analyzer** is a **Streamlit** web application that provides a detailed analysis of baseball hits, focusing on key metrics such as **Exit Velocity**, **Launch Angle**, and **Hit Distance**. The app also allows users to explore player statistics, compare players' performance, and even predict the exit velocity for future hits based on historical data.

### Key Features:
- 🔍 **Interactive Data Exploration**: Allows users to filter and analyze data by selecting multiple players.
- 📊 **Visualization**: Scatter plots showing the relationship between Exit Velocity and Hit Distance.
- 🌍 **Language Support**: Provides data insights in **English**, **Spanish**, and **Japanese**.
- 🧑‍💼 **Player Statistics**: Displays player-specific statistics including Average Exit Velocity, Median Launch Angle, and Home Run counts.
- 🏅 **Top Performances**: Showcases the top 10 home runs based on Exit Velocity and Hit Distance.
- 📊 **Stat Comparison**: Allows side-by-side comparison of players' statistics.
- ⭐ **Save Favorites**: Users can save their favorite players for future reference.
- 🔮 **Predictive Model**: Includes a basic linear regression model to predict the Exit Velocity for future hits based on Launch Angle and Hit Distance.
- 🎥 **Video Integration**: Allows users to watch videos of selected hits.

## Requirements

To run the **Baseball Hit Analyzer**, the following Python libraries are required:

- `pandas`
- `streamlit`
- `matplotlib`
- `scikit-learn`

You can install the required libraries using `pip`:

```bash
pip install pandas streamlit matplotlib scikit-learn
