from django.shortcuts import render
import json
import requests
from datetime import datetime
from clothes.local_settings import location_key, dark_key

def weather(request):
    place = ""

    if request.method == "POST":
        place = request.POST.get("location")
    else:
        place = "Belfast"
    

    # Location api
    loc_api = location_api
    loc_api_url = "https://api.opencagedata.com/geocode/v1/json?q=%s&key=%s" % (place, loc_api)
    loc_res = requests.get(loc_api_url)
    loc_data = loc_res.json()

    loc_results = loc_data['total_results']

    if loc_results < 1:
        place = "Belfast"
        loc_api_url = "https://api.opencagedata.com/geocode/v1/json?q=%s&key=%s" % (place, loc_api)
        loc_res = requests.get(loc_api_url)
        loc_data = loc_res.json()

    location = (place.capitalize()) + ", " + loc_data['results'][0]['components']['state']
    

    try:
        town = loc_data['results'][0]['components']['village']
    except Exception:
        town = place.capitalize()

    lon = loc_data['results'][0]['geometry']['lng']
    lat = loc_data['results'][0]['geometry']['lat']


    # Weather api
    api_key = dark_key
    api_url = "https://api.darksky.net/forecast/%s/%s,%s?exclude=minutely,alerts,flags,daily&units=si" % (api_key, lat, lon)

    res = requests.get(api_url)
    data = res.json()

    current = {
        "time": datetime.fromtimestamp(data['currently']['time']),
        "summary": data['currently']['summary'],
        "wind": data['currently']['windSpeed'],
        "temp": data['currently']['temperature'],
        "humidity": data['currently']['humidity'],
        "rainChance": data['currently']['precipProbability']
    }

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

        nextHours.append({
            "time": datetime.fromtimestamp(h['time']),
            "icon": icon,
            "summary": h['summary'],
            "wind": h['windSpeed'],
            "temp": h['temperature'],
            "humidity": h['humidity'],
            "rainChance": h['precipProbability'],
            "should": should
        })


    h = nextHours[0]['humidity']

    dryTime = (2*h**2)+(80*h)+40

    context = {
        "hour": nextHours[0],
        "location": location,
        "town": town,
        "dry": dryTime,
        "forecast": nextHours[1:4]
    }
    return render(request, 'api/weather.html', context)