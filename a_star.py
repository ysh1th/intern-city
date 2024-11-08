from math import radians, sin, cos, sqrt, atan2
import streamlit as st
import numpy as np
import heapq

class Node:
    def __init__(self, company, g, h , w_proximity, w_skills):
        self.company = company 
        self.g = g              
        self.h = h              
        self.f = w_proximity * g + w_skills * h

    def __lt__(self, other):
        return self.f < other.f 
    
# normalizing to scale distances b/w 0 & 1
def normalize(values):
    max_value = max(values)
    return [v / max_value if max_value != 0 else 0 for v in values]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # dist in km
    distance = R * c
    return distance

@st.cache_data
def a_star_algorithm(companies, user_location, user_skills, w_proximity, w_skills):
    open_set = []
    closed_set = set()
    distances = []
    results = []

    user_skills = set([skill.lower() for skill in user_skills])
    
    for company in companies:
        lat, long = company['latitude'], company['longitude']
        distance = haversine(user_location[0], user_location[1], lat, long)
        distances.append(distance)
        
        company_skills = set([skill.lower() for skill in company.get('skills', [])])
        skill_match_score = len(user_skills & company_skills) / len(user_skills)
        
        if skill_match_score > 0:
            h = 1 - skill_match_score
            node = Node(company, distance, h, w_proximity, w_skills)
            heapq.heappush(open_set, node)

    # normalized_distances = normalize(distances)

    while open_set and len(results) < 5:
        current_node = heapq.heappop(open_set)
        company = current_node.company
        distance = haversine(user_location[0], user_location[1], company['latitude'], company['longitude'])
        
        company_skills = set([skill.lower() for skill in company.get('skills', [])])
        skill_match_score = len(user_skills & company_skills) / len(user_skills)
        
        normalized_distance = distance / max(distances) 
        final_score = w_proximity * normalized_distance + w_skills * (1 - skill_match_score)
        
        if company['Company Name'] not in closed_set:
            closed_set.add(company['Company Name'])
            results.append({
                'company': company,
                'distance': distance,
                'final_score': final_score
            })

    results.sort(key=lambda x: x['final_score'])
    
    return results