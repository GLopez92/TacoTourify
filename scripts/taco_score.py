# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:12:11 2024

@author: GuillermoLopez
"""

import matplotlib.pyplot as plt
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Spotify API authentication
client_credentials_manager = SpotifyClientCredentials(
    client_id='xxxxxxxx', 
    client_secret='xxxxxxxx'
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Fetch artist's top tracks
results = sp.artist_top_tracks('7aKKl2wFvnHgKNdEpORCMK', country='US')
print(results)

# Mock Spotify listener data
spotify_data = pd.DataFrame({
    'City': ['Los Angeles', 'New York', 'Austin', 'San Diego', 'Chicago'],
    'Listeners': [10000, 12000, 8000, 7000, 9500]
})

# Mock taco truck data
taco_data = pd.DataFrame({
    'City': ['Los Angeles', 'New York', 'Austin', 'San Diego', 'Chicago'],
    'Taco_Truck_Count': [10, 7, 15, 5, 8]
})

# Adjust listener counts based on city population
population_data = pd.DataFrame({
    'City': ['Los Angeles', 'New York', 'Austin', 'San Diego', 'Chicago'],
    'Population': [3980000, 8419000, 964000, 1424000, 2716000]
})

# Merge population and listener data
enhanced_data = pd.merge(spotify_data, population_data, on='City')
enhanced_data['Adjusted_Listeners'] = enhanced_data['Listeners'] * (enhanced_data['Population'] / enhanced_data['Population'].sum())

# Merge enhanced data with taco truck data
combined_data = pd.merge(enhanced_data, taco_data, on='City')

# Calculate Taco Score
combined_data['Taco_Score'] = combined_data['Adjusted_Listeners'] * combined_data['Taco_Truck_Count']

# Rank cities based on Taco Score
ranked_data = combined_data.sort_values(by='Taco_Score', ascending=False)

# Visualization
plt.figure(figsize=(10, 6))
plt.bar(ranked_data['City'], ranked_data['Taco_Score'], color='skyblue')
plt.xlabel('City', fontsize=12)
plt.ylabel('Taco Score (Adjusted Listeners × Taco Trucks)', fontsize=12)
plt.title('Top Cities for Tacos and Music Tours', fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



