import os
import streamlit as st
import folium
import polyline
import googlemaps
from datetime import datetime
from dotenv import load_dotenv
from streamlit_folium import st_folium
import heapq
from math import radians, sin, cos, sqrt, atan2

# Google Maps API key
load_dotenv()
gmaps_api_key = os.getenv('GOOGLE_MAPS_API')
gmaps = googlemaps.Client(key=gmaps_api_key)

# def create_map(center=[25.1325, 55.4201], zoom=15):
#     """Create a folium map for location selection"""
#     m = folium.Map(location=center, zoom_start=zoom)
#     return m

def create_map(center=[25.1325, 55.4201], zoom=15):
    m = folium.Map(location=center, zoom_start = zoom)
    folium.ClickForMarker().add_to(m)
    return m

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

class Node:
    def __init__(self, company, g, h, w_proximity, w_skills):
        self.company = company
        self.g = g
        self.h = h
        self.f = w_proximity * g + w_skills * h

    def __lt__(self, other):
        return self.f < other.f

def get_unique_skills(internships):
    """Extract unique skills from all internships"""
    skills_set = set()
    for internship in internships:
        skills_set.update([skill.lower() for skill in internship.get('skills', [])])
    return sorted(list(skills_set))

def a_star_algorithm(companies, user_location, user_skills, w_proximity, w_skills):
    open_set = []
    closed_set = set()
    results = []

    user_skills = set([skill.lower() for skill in user_skills])
    
    for company in companies:
        lat, lon = company['latitude'], company['longitude']
        distance = haversine_distance(user_location[0], user_location[1], lat, lon)
        
        company_skills = set([skill.lower() for skill in company.get('skills', [])])
        skill_match_score = len(user_skills & company_skills) / len(user_skills) if len(user_skills) > 0 else 0
        h = 1 - skill_match_score

        if skill_match_score > 0:
            node = Node(company, distance, h, w_proximity, w_skills)
            heapq.heappush(open_set, node)

    while open_set and len(results) < 5:
        current_node = heapq.heappop(open_set)
        company = current_node.company
        
        if company['Company Name'] not in closed_set:
            closed_set.add(company['Company Name'])
            results.append({
                'company': company,
                'distance': current_node.g,
                'final_score': current_node.f
            })

    results.sort(key=lambda x: x['final_score'])
    return results

def visualize_internships(user_location, nearby_internships):
    map = folium.Map(location=user_location, zoom_start=12)
    
    # Add user location marker
    folium.Marker(
        user_location,
        popup="Your Location",
        icon=folium.Icon(color='red')
    ).add_to(map)
    
    for internship in nearby_internships:
        company = internship['company']
        distance = internship['distance']
        folium.Marker(
            [company['latitude'], company['longitude']],
            popup=f"{company['title']} at {company['Company Name']}<br>Distance: {distance:.2f} km<br>Score: {internship['final_score']:.2f}",
            icon=folium.Icon(color='blue')
        ).add_to(map)

    return map._repr_html_()

def main():
    st.title("Internship Finder & Route Visualizer")

    # Sample internships data
    internships = [
    {
        'Company Name': 'ESRI',
        'title': 'Software Engineering Intern',
        'latitude': 25.3297,
        'longitude': 55.3913,
        'skills': ["GIS", "Python", "Security", "Java", "Machine Learning"]
    },
    {
        'Company Name': 'Google',
        'title': 'Software Engineering Intern',
        'latitude': 25.197525,
        'longitude': 55.274288,
        'skills': ['Python', 'Machine Learning', 'AI', 'Cloud', 'Mobile Development']
    },
    {
        'Company Name': 'Microsoft',
        'title': 'Data Science Intern',
        'latitude': 25.234511,
        'longitude': 55.324905,
        'skills': ['Python', 'Java', 'SQL', 'Machine Learning', 'AI']
    },
    {
        'Company Name': 'IBM',
        'title': 'Cloud Solutions Intern',
        'latitude': 25.276987,
        'longitude': 55.296249,
        'skills': ['Java', 'Cloud', 'Security', 'Blockchain']
    },
    {
        'Company Name': 'Amazon Web Services',
        'title': 'Cloud Engineering Intern',
        'latitude': 25.211234,
        'longitude': 55.283456,
        'skills': ['Cloud Computing', 'DevOps', 'Big Data']
    },
    {
        'Company Name': 'Nvidia',
        'title': 'AI Research Intern',
        'latitude': 25.265432,
        'longitude': 55.312345,
        'skills': ['GPU Computing', 'Machine Learning', 'Deep Learning']
    },
    {
        'Company Name': 'Adobe',
        'title': 'UX/UI Design Intern',
        'latitude': 25.243567,
        'longitude': 55.298765,
        'skills': ['UX/UI Design', 'Digital Marketing', 'Cloud Services']
    },
    {
        'Company Name': 'Oracle',
        'title': 'Database Development Intern',
        'latitude': 25.222345,
        'longitude': 55.289876,
        'skills': ['SQL', 'DBMS', 'Java', 'Cloud Infrastructure']
    },
    {
        'Company Name': 'Cisco Systems',
        'title': 'Network Engineering Intern',
        'latitude': 25.254567,
        'longitude': 55.301234,
        'skills': ['Networking', 'Security', 'IoT', 'Python']
    },
    {
        'Company Name': 'SAP',
        'title': 'ERP Development Intern',
        'latitude': 25.287654,
        'longitude': 55.334567,
        'skills': ['ERP', 'ABAP', 'Cloud', 'Data Analytics']
    },
    {
        'Company Name': 'Huawei',
        'title': '5G Technology Intern',
        'latitude': 25.198765,
        'longitude': 55.287654,
        'skills': ['5G', 'AI', 'Cloud Computing', 'IoT']
    },
    {
        'Company Name': 'Salesforce',
        'title': 'CRM Development Intern',
        'latitude': 25.245678,
        'longitude': 55.323456,
        'skills': ['CRM', 'Cloud Computing', 'AI']
    },
    {
        'Company Name': 'Intel',
        'title': 'Hardware Engineering Intern',
        'latitude': 25.267890,
        'longitude': 55.345678,
        'skills': ['Hardware Design', 'AI', 'IoT', 'Cloud Computing']
    },
    {
        'Company Name': 'Careem',
        'title': 'Mobile Development Intern',
        'latitude': 25.234567,
        'longitude': 55.290123,
        'skills': ['Mobile Development', 'AI', 'Data Science']
    },
    {
        'Company Name': 'Noon',
        'title': 'E-commerce Development Intern',
        'latitude': 25.256789,
        'longitude': 55.312345,
        'skills': ['E-commerce', 'Mobile Development', 'AI']
    },
    {
        'Company Name': 'Mastercard',
        'title': 'Fintech Development Intern',
        'latitude': 25.289012,
        'longitude': 55.334567,
        'skills': ['Fintech', 'Cybersecurity', 'Blockchain']
    },
    {
        'Company Name': 'Accenture',
        'title': 'Technology Consulting Intern',
        'latitude': 25.223456,
        'longitude': 55.287654,
        'skills': ['Consulting', 'AI', 'Blockchain', 'Cloud']
    },
    {
        'Company Name': 'Infosys',
        'title': 'Software Development Intern',
        'latitude': 25.245678,
        'longitude': 55.301234,
        'skills': ['Software Development', 'Cloud Computing', 'Data Analytics']
    },
    {
        'Company Name': 'Dell Technologies',
        'title': 'Cloud Infrastructure Intern',
        'latitude': 25.267890,
        'longitude': 55.323456,
        'skills': ['Cloud Computing', 'Virtualization', 'Data Storage']
    },
    {
        'Company Name': 'Siemens',
        'title': 'Industrial IoT Intern',
        'latitude': 25.212345,
        'longitude': 55.289012,
        'skills': ['IoT', 'Automation', 'Industrial Software']
    },
    {
        'Company Name': 'HP Inc.',
        'title': '3D Technology Intern',
        'latitude': 25.234567,
        'longitude': 55.312345,
        'skills': ['Hardware Engineering', '3D Printing', 'AI']
    },
    {
        'Company Name': 'Autodesk',
        'title': 'CAD Development Intern',
        'latitude': 25.256789,
        'longitude': 55.334567,
        'skills': ['CAD', '3D Modeling', 'Cloud-based Design']
    },
    {
        'Company Name': 'Bosch',
        'title': 'IoT Development Intern',
        'latitude': 25.278901,
        'longitude': 55.356789,
        'skills': ['IoT', 'Automotive Technology', 'AI']
    },
    {
        'Company Name': 'GE Digital',
        'title': 'Industrial Digital Intern',
        'latitude': 25.223456,
        'longitude': 55.301234,
        'skills': ['Industrial IoT', 'Data Analytics', 'Cloud Platforms']
    },
    {
        'Company Name': 'Etisalat Digital',
        'title': 'Telecommunications Intern',
        'latitude': 25.245678,
        'longitude': 55.323456,
        'skills': ['Telecommunications', '5G', 'Digital Transformation']
    },
    {
        'Company Name': 'Souq.com (Amazon)',
        'title': 'E-commerce Development Intern',
        'latitude': 25.267890,
        'longitude': 55.345678,
        'skills': ['E-commerce', 'Web Development', 'Data Analytics']
    }
]

    # Display map for location selection
    with st.expander("Select Your Location", expanded=True):
      st.header("Select Your Location")
      m = create_map()
      map_data = st_folium(m, width=725, height=500)


# if 'expanded' not in st.session_state:
#     st.session_state['expanded'] = True

# with st.expander("Select Your Location", expanded=st.session_state['expanded']):
#     m = create_map()
#     map_data = st_folium(m, width=725, height=500)
    
#     # Check if a location is selected
#     if map_data and 'coordinates' in map_data:
#         st.session_state['expanded'] = False  # Collapse the section

    # Initialize session state for user location if not exists
    if 'user_location' not in st.session_state:
        st.session_state['user_location'] = None

    # Update user location when map is clicked
    if map_data and 'last_clicked' in map_data:
        clicked_location = map_data['last_clicked']
        st.session_state['user_location'] = clicked_location

    # Sidebar inputs
    st.sidebar.header("Preferences")
    
    # Get unique skills from internships and create multi-select
    available_skills = get_unique_skills(internships)
    selected_skills = st.sidebar.multiselect(
        "Select Your Skills",
        options=available_skills,
        default=None
    )

    # Weights for proximity and skills
    w_proximity = st.sidebar.slider("Weight for Proximity", 0.0, 1.0, 0.5)
    w_skills = st.sidebar.slider("Weight for Skills Match", 0.0, 1.0, 0.5)

    # Process search only if location is selected and skills are chosen
    if st.session_state['user_location'] is not None and selected_skills:
        user_lat = st.session_state['user_location']['lat']
        user_long = st.session_state['user_location']['lng']
        user_location = (user_lat, user_long)

        # Find and display nearby internships
        st.header("Nearby Internships")
        nearby_internships = a_star_algorithm(internships, user_location, selected_skills, w_proximity, w_skills)
        
        if nearby_internships:
            map_html = visualize_internships(user_location, nearby_internships)
            st.components.v1.html(map_html, height=500)

            # Display internship selection and route
            st.subheader("Select an Internship to View Route")
            selected_internship = st.selectbox(
                "Internship",
                options=[f"{internship['company']['title']} at {internship['company']['Company Name']}" for internship in nearby_internships]
            )

            if selected_internship:
                internship_data = next(intern['company'] for intern in nearby_internships 
                                     if f"{intern['company']['title']} at {intern['company']['Company Name']}" == selected_internship)

                if st.button("Show Route"):
                    steps = gmaps.directions(
                        f"{user_lat},{user_long}",
                        f"{internship_data['latitude']},{internship_data['longitude']}",
                        mode="driving",
                        language="en",
                        departure_time=datetime.now()
                    )
                    
                    if steps:
                        route_map = folium.Map(location=user_location, zoom_start=13)
                        folium.Marker(
                            user_location, popup="Your Location", icon=folium.Icon(color='red')
                        ).add_to(route_map)
                        
                        folium.Marker(
                            [internship_data['latitude'], internship_data['longitude']], 
                            popup=internship_data['title'], 
                            icon=folium.Icon(color='blue')
                        ).add_to(route_map)
                        
                        for step in steps[0]['legs'][0]['steps']:
                            path = polyline.decode(step['polyline']['points'])
                            folium.PolyLine(locations=path, color='red', weight=5, opacity=0.7).add_to(route_map)
                        
                        route_map_html = route_map._repr_html_()
                        st.components.v1.html(route_map_html, height=500)
                        st.success(f"Route to {internship_data['title']} at {internship_data['Company Name']}")
        else:
            st.warning("No matching internships found. Try adjusting your skills or weights.")
    else:
        if st.session_state['user_location'] is None:
            st.info("Please select your location on the map.")
        if not selected_skills:
            st.info("Please select at least one skill from the sidebar.")

if __name__ == "__main__":
    main()