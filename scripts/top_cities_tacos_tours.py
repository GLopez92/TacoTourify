# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 18:36:10 2024

@author: GuillermoLopez
"""

import pandas as pd
import matplotlib.pyplot as plt

spotify_data = pd.DataFrame({
    'City': ['Los Angeles', 'Austin', 'New York', 'Chicago', 'San Diego'],
    'Listeners': [10000, 8000, 12000, 9500, 7000]
})

taco_data = pd.DataFrame({
    'City': ['Los Angeles', 'Austin', 'New York', 'Chicago', 'San Diego'],
    'Taco_Truck_Count': [50, 60, 45, 30, 40]
})

combined_data = pd.merge(spotify_data, taco_data, on='City')
combined_data['Taco_Score'] = combined_data['Listeners'] * combined_data['Taco_Truck_Count']
print(combined_data)

# Sort data by Taco_Score
combined_data = combined_data.sort_values('Taco_Score', ascending=False)

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(combined_data['City'], combined_data['Taco_Score'], color='skyblue')
plt.xlabel('City')
plt.ylabel('Taco Score')
plt.title('Top Cities for Tacos and Tours')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.savefig('top_cities_tacos_tours.png')
