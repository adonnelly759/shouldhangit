import requests
import json
from datetime import datetime

def get_data(place, oc_api, ds_api):
    # Open Cage API
    loc_api_url = "https://api.opencagedata.com/geocode/v1/json?q=%s&key=%s" % (place, oc_api)
    loc_res = requests.get(loc_api_url)
    loc_data = loc_res.json()
    loc_results = loc_data['total_results']
    loc_results = loc_data['total_results']

    if loc_results < 1:
        place = "Belfast"
        loc_api_url = "https://api.opencagedata.com/geocode/v1/json?q=%s&key=%s" % (place, oc_api)
        loc_res = requests.get(loc_api_url)
        loc_data = loc_res.json()

    lon = loc_data['results'][0]['geometry']['lng']
    lat = loc_data['results'][0]['geometry']['lat']

    # Dark Sky API
    api_url = "https://api.darksky.net/forecast/%s/%s,%s?exclude=minutely,alerts,flags,daily&units=si" % (ds_api, lat, lon)

    res = requests.get(api_url)
    data = res.json()
    return data

def get_next(data, place):
    # Create empty list for future hours
    nextHours = []
    # Stores next 48 hours + current hour
    hourlyData = data['hourly']

    # Loop to append this data
    for h in hourlyData['data']:
        tempMark = 0

        # Assign marks depending on weather
        if h['windSpeed'] > 5 and h['precipProbability'] < 0.4:
            tempMark += 1
        
        if h['temperature'] > 5 and h['precipProbability'] < 0.4: 
            tempMark += 1

        if h['humidity'] < 0.7 and h['precipProbability'] < 0.4:
            tempMark += 1

        should = 0

        icon = ""

        # Get icon
        if h['icon'] == "clear-day":
            icon = "sun"
        elif h['icon'] == "clear-night":
            icon = "sun"
        elif h['icon'] == "rain":
            icon = "water"
        elif h['icon'] == "sleet":
            icon = "water"
        elif h['icon'] == "snow":
            icon = "snowflake"
        elif h['icon'] == "fog":
            icon = "cloud"
        elif h['icon'] == "cloudy":
            icon = "cloud"
        else:
            icon = "cloud"

        # Return should we value
        if tempMark == 0:
            should = "You having a laugh?"

        if tempMark == 1:
            should = "Not now!"
        
        if tempMark == 2:
            should = "Why not?"

        if tempMark == 3: 
            should = "Hang it out!"

        x = h['humidity']

        nextHours.append({
            "time": datetime.fromtimestamp(h['time']),
            "icon": icon,
            "summary": h['summary'],
            "wind": h['windSpeed'],
            "temp": h['temperature'],
            "humidity": h['humidity'],
            "rainChance": h['precipProbability'],
            "should": should,
            "dryTime": (2*x**2)+(80*x)+40
        })
    return nextHours