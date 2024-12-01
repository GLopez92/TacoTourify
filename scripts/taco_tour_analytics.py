# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:19:39 2024

@author: GuillermoLopez
"""
import folium
import matplotlib.pyplot as plt
import pandas as pd
from geopy.geocoders import Nominatim
import time
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Spotify API authentication
client_credentials_manager = SpotifyClientCredentials(
    client_id='xxxxxxxx',
    client_secret='xxxxxxxx'
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Fetch artist's top tracks (mock API call)
results = sp.artist_top_tracks('7aKKl2wFvnHgKNdEpORCMK', country='US')
print(results)  # Optional: Remove if not used

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

# Mock population data
population_data = pd.DataFrame({
    'City': ['Los Angeles', 'New York', 'Austin', 'San Diego', 'Chicago'],
    'Population': [3980000, 8419000, 964000, 1424000, 2716000]
})

# Merge listener, taco truck, and population data
combined_data = pd.merge(spotify_data, taco_data, on='City')
combined_data = pd.merge(combined_data, population_data, on='City')

# Initialize geolocator for dynamic geocoding
geolocator = Nominatim(user_agent="geoapi")

def get_coordinates(city_name):
    location = geolocator.geocode(city_name)
    time.sleep(1)  # Add delay to respect API rate limits
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Fetch coordinates and add to DataFrame
combined_data['Latitude'], combined_data['Longitude'] = zip(*combined_data['City'].apply(get_coordinates))
combined_data = combined_data.dropna(subset=['Latitude', 'Longitude'])  # Drop rows with missing coordinates

# Calculate adjusted listeners and Taco Score
combined_data['Adjusted_Listeners'] = combined_data['Listeners'] * (combined_data['Population'] / combined_data['Population'].sum())
combined_data['Taco_Score'] = combined_data['Listeners'] * combined_data['Taco_Truck_Count']

# Bar chart of top cities by Taco Score
ranked_data = combined_data.sort_values(by='Taco_Score', ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.bar(ranked_data['City'], ranked_data['Taco_Score'], color='skyblue')
plt.xlabel('City', fontsize=12)
plt.ylabel('Taco Score (Listeners × Taco Trucks)', fontsize=12)
plt.title('Top 10 Cities by Taco Score', fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Create a dynamic Folium map centered on the mean coordinates
map_center = [combined_data['Latitude'].mean(), combined_data['Longitude'].mean()]
map_choropleth = folium.Map(location=map_center, zoom_start=4)

# Add markers for each city
for _, row in combined_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=10,  # Size of the circle
        popup=folium.Popup(
            f"{row['City']}<br>Listeners: {row['Listeners']}<br>"
            f"Taco Trucks: {row['Taco_Truck_Count']}<br>"
            f"Taco Score: {row['Taco_Score']}",
            max_width=250
        ),
        color='blue',
        fill=True,
        fill_color='skyblue',
        fill_opacity=0.7
    ).add_to(map_choropleth)

# Save the map
map_choropleth.save('choropleth_map.html')



