import os
import streamlit as st
import pandas as pd
import googlemaps
from streamlit_folium import st_folium  # Ensure this is imported correctly
import folium
from dotenv import load_dotenv
load_dotenv()

gmaps_api_key = os.getenv('GOOGLE_MAPS_API')  # google maps api key is stored in .env file

gmaps = googlemaps.Client(key=gmaps_api_key)
st.title("Location-Based Internship Finder")

def create_map():
    # Initial map centered on BPDC
    m = folium.Map(location=[25.1325, 55.4201], zoom_start=15)
    
    # Add ClickForMarker functionality with popup for clicked location
    folium.ClickForMarker().add_to(m)
    
    return m

# Display the map in Streamlit and allow user to click
m = create_map()

# Use st_folium to display the map
map_data = st_folium(m, width=725, height=500)  # Correct usage

# Check if user clicked on the map
if map_data and 'last_clicked' in map_data:
    clicked_location = map_data['last_clicked']
    st.write(f"Clicked location: {clicked_location}")

    # Store clicked location in session state
    st.session_state['user_location'] = clicked_location

if 'user_location' in st.session_state and st.session_state['user_location'] is not None:
    lat, lng = st.session_state['user_location']['lat'], st.session_state['user_location']['lng']
    st.write(f"Latitude: {lat}, Longitude: {lng}")

    # Reverse geocode to get the place ID
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))

    if reverse_geocode_result:
        place_id = reverse_geocode_result[0]['place_id']
        st.write(f'Place ID: {place_id}')
    else:
        st.write('Could not retrieve place ID.')
