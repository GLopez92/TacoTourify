# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 19:36:27 2024

@author: GuillermoLopez
"""
import matplotlib.pyplot as plt
import pandas as pd
import random
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import folium
from datetime import datetime

# Spotify API authentication
client_credentials_manager = SpotifyClientCredentials(
    client_id='xxxxxxxx',
    client_secret='xxxxxxxx'
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Taco Facts
taco_facts = [
    "The world's largest taco was 246 feet long and made in Mexico City.",
    "Taco Bell was originally named 'Taco Tia.'",
    "Americans eat over 4.5 billion tacos every year.",
    "The word 'taco' translates to 'plug' or 'wad' in Spanish.",
    "National Taco Day is celebrated on October 4th."
]

def get_random_taco_fact():
    return random.choice(taco_facts)

# Mock Spotify listener data
combined_data = pd.DataFrame({
    'City': ['Los Angeles', 'New York', 'Austin', 'San Diego', 'Chicago'],
    'Listeners': [10000, 12000, 8000, 7000, 9500],
    'Taco_Truck_Count': [10, 7, 15, 5, 8]
})

# Add latitude and longitude for cities
city_coordinates = {
    'Los Angeles': [34.0522, -118.2437],
    'New York': [40.7128, -74.0060],
    'Austin': [30.2672, -97.7431],
    'San Diego': [32.7157, -117.1611],
    'Chicago': [41.8781, -87.6298]
}
combined_data['Latitude'] = combined_data['City'].map(lambda city: city_coordinates[city][0])
combined_data['Longitude'] = combined_data['City'].map(lambda city: city_coordinates[city][1])

# Mock historical listener data for trend calculation
historical_data = pd.DataFrame({
    'City': ['Los Angeles', 'New York', 'Austin', 'San Diego', 'Chicago'],
    'Listeners_Jan': [9000, 11000, 7500, 6800, 9200],
    'Listeners_Mar': [10000, 12000, 8500, 7300, 9700]
})

# Calculate Listener Growth Trend
historical_data['Trend'] = (historical_data['Listeners_Mar'] - historical_data['Listeners_Jan']) / historical_data['Listeners_Jan']
combined_data = pd.merge(combined_data, historical_data[['City', 'Trend']], on='City')

# Calculate Trend-Adjusted Listeners
combined_data['Trend_Adjusted_Listeners'] = combined_data['Listeners'] * (1 + combined_data['Trend'])

# Calculate Predicted Streams
boost_factor = 0.1  # Hypothetical boost factor
combined_data['Predicted_Streams'] = combined_data['Trend_Adjusted_Listeners'] + (
    combined_data['Taco_Truck_Count'] * combined_data['Trend_Adjusted_Listeners'] * boost_factor
)

# Bar Plot Function
def plot_streams(data, title):
    bar_width = 0.25
    index = range(len(data))
    plt.figure(figsize=(12, 6))

    # Current streams
    plt.bar(index, data['Listeners'], bar_width, label='Current Streams', color='skyblue')

    # Trend-adjusted listeners
    plt.bar(
        [i + bar_width for i in index],
        data['Trend_Adjusted_Listeners'],
        bar_width,
        label='Trend-Adjusted Listeners',
        color='orange'
    )

    # Predicted streams
    plt.bar(
        [i + 2 * bar_width for i in index],
        data['Predicted_Streams'],
        bar_width,
        label='Predicted Streams',
        color='lightgreen'
    )

    plt.xlabel('City', fontsize=12)
    plt.ylabel('Streams', fontsize=12)
    plt.title(title, fontsize=16)
    plt.xticks([i + bar_width for i in index], data['City'], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plotting Streams
plot_streams(combined_data, 'Current vs Trend-Adjusted vs Predicted Stream Boosts')

# Listener Trends Line Plot
months = ['Jan', 'Mar']  # Dynamically reference column names if needed
plt.figure(figsize=(12, 6))
for city in historical_data['City']:
    city_data = historical_data[historical_data['City'] == city]
    plt.plot(months, city_data.iloc[0, 1:3], label=city)
plt.xlabel('Month')
plt.ylabel('Listeners')
plt.title('Listener Trends Over Time')
plt.legend()
plt.tight_layout()
plt.show()

# Folium Map
map_choropleth = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
for _, row in combined_data.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=10,
        popup=folium.Popup(
            f"{row['City']}<br>Listeners: {row['Listeners']}<br>"
            f"Taco Trucks: {row['Taco_Truck_Count']}<br>"
            f"Taco Score: {row['Predicted_Streams']}<br>"
            f"Random Fact: {get_random_taco_fact()}",
            max_width=250
        ),
        color='blue',
        fill=True,
        fill_color='skyblue',
        fill_opacity=0.7
    ).add_to(map_choropleth)

# Generate a unique filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'taco_tour_map_{timestamp}.html'
map_choropleth.save(filename)
print(f"Map saved as {filename}")





