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

# declaring global variables
user_lat, user_long = None, None 

def create_map():
    # Initial map centered on BPDC
    m = folium.Map(location=[25.1325, 55.4201], zoom_start=15)
    
    # Add ClickForMarker functionality with popup for clicked location
    folium.ClickForMarker().add_to(m)
    
    return m

# Display the map in Streamlit and allow user to click
m = create_map()

# Use st_folium to display the map
map_data = st_folium(m, width=725, height=200) 

# Check if user clicked on the map
if map_data and 'last_clicked' in map_data:
    clicked_location = map_data['last_clicked']
    # st.write(f"Clicked location: {clicked_location}")

    # Store clicked location in session state
    st.session_state['user_location'] = clicked_location

if 'user_location' in st.session_state and st.session_state['user_location'] is not None:
    user_lat, user_long = st.session_state['user_location']['lat'], st.session_state['user_location']['lng']
    st.write(f"Latitude: {user_lat}, Longitude: {user_long}")

    # Reverse geocode to get the place ID
    reverse_geocode_result = gmaps.reverse_geocode((user_lat, user_long))

    if reverse_geocode_result:
        place_id = reverse_geocode_result[0]['place_id']
        st.write(f'Place ID: {place_id}')
    else:
        st.write('Could not retrieve place ID.')

# web scraping code goes here

# tests for company geocodes fetch
tech_companies = [
    {"Company Name": "Microsoft", "City": "Dubai"},
    {"Company Name": "Google", "City": "Dubai"},
    {"Company Name": "IBM", "City": "Dubai"},
    {"Company Name": "Oracle", "City": "Dubai"},
    {"Company Name": "Cisco Systems", "City": "Dubai"},
    {"Company Name": "Esri", "City": "Sharjah"},
    
]
# code to output api data (to know the structure of api)
# first_company = tech_companies[0]

# geocode_result = gmaps.geocode(first_company["Company Name"] + ',' + first_company['City'])

# st.write(f"Geocode result for {first_company['Company Name']}:")
# st.write(geocode_result)

def get_lat_long(company_name, company_city):
    try: 
        # use place autocomplete to get precise result
        autocomplete_result = gmaps.places_autocomplete(company_name + ',' + company_city, types='establishment')

        if autocomplete_result:
            company_place_id = autocomplete_result[0]['place_id']
            place_details = gmaps.place(place_id = company_place_id)

            # extract lat and long from place details
            lat = place_details['result']['geometry']['location']['lat']
            long = place_details['result']['geometry']['location']['lng']
            address = place_details['result'].get('formatted_address', 'No address found')

            return company_place_id, lat, long, address

    except Exception as e:
        st.write(f'Error retrieving location for {company_name}: {e}')
    return None, None

for company in tech_companies:
    place_id, lat, long, address = get_lat_long(company["Company Name"], company['City'])
    company['place id'] = place_id
    company["latitude"] = lat
    company["longitude"] = long
    company["address"] = address

df = pd.DataFrame(tech_companies)

st.title("tech companies with lat and long")
st.dataframe(df)