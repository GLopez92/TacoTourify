# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 18:46:25 2024

@author: GuillermoLopez
"""
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely.geometry import Point
import folium

# Spotify API authentication
client_credentials_manager = SpotifyClientCredentials(
    client_id='xxxxxxxx', 
    client_secret='xxxxxxxx'
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Fetch artist's top tracks
results = sp.artist_top_tracks('7aKKl2wFvnHgKNdEpORCMK')
print(results)

# Mock Spotify listener data
data = {
    'City': ['City A', 'City B', 'City C'],
    'Listeners': [5000, 3000, 4500]
}
spotify_data = pd.DataFrame(data)

# Mock taco truck data (manually created instead of Yelp API)
taco_data = pd.DataFrame({
    'City': ['City A', 'City B', 'City C'],
    'Taco_Truck_Count': [10, 7, 15]
})

# Combine Spotify listener data and taco truck data
combined_data = pd.merge(spotify_data, taco_data, on='City')
combined_data['Taco_Score'] = combined_data['Listeners'] * combined_data['Taco_Truck_Count']

# Add geographic coordinates using GeoPy (mocked for example)
geolocator = Nominatim(user_agent="geoapi")
coordinates = {
    'City A': (34.0522, -118.2437),
    'City B': (40.7128, -74.0060),
    'City C': (37.7749, -122.4194)
}
combined_data['Latitude'] = combined_data['City'].apply(lambda city: coordinates[city][0])
combined_data['Longitude'] = combined_data['City'].apply(lambda city: coordinates[city][1])

# Convert to GeoDataFrame
combined_data['Coordinates'] = combined_data.apply(
    lambda row: Point(row['Longitude'], row['Latitude']), axis=1
)
gdf = gpd.GeoDataFrame(combined_data, geometry='Coordinates')

# Create an interactive map with Folium
map = folium.Map(location=[37.7749, -122.4194], zoom_start=5)
for _, row in gdf.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['City']}: {row['Listeners']} listeners, {row['Taco_Truck_Count']} taco trucks",
    ).add_to(map)

# Save the map to an HTML file
map.save('taco_tour_map.html')

print("Map saved as 'taco_tour_map.html'")

