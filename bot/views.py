from django.shortcuts import render_to_response
from django.conf import settings

from bot.models import FoodTruckEvents, FoodTruck
from bot.trucks import get_truck_frequency

from datetime import datetime
import requests
import json
import re


def home(request):
    """home page view"""
    truck_list = get_truck_frequency()
    variables = {
        'truck_list': truck_list}
    return render_to_response('home.html', variables)


def daily_job():
    """runs the a job daily to get food truck on that day"""
    try:
        with open('simple.json') as infile:
            data = json.load(infile)
    except IOError:
        url = 'https://graph.facebook.com/129511477069092/events?access_token=' + settings.FACEBOOK_ACCESS_TOKEN
        #print url
        req = requests.get(url)
        data = req.json()
        with open('simple.json', 'w') as outfile:
            json.dump(data, outfile)

    for event in data["data"]:
        name = event["name"]
        location = event["location"]

        try:
            start_time = (datetime.datetime.strptime(event["start_time"][:-5], '%Y-%m-%dT%H:%M:%S')).strftime("%Y-%m-%d %H:%M")
            if 'end_time' in event:
                end_time = (datetime.datetime.strptime(event["end_time"][:-5], '%Y-%m-%dT%H:%M:%S')).strftime("%Y-%m-%d %H:%M")
            else:
                end_time = None
        except ValueError:
            start_time = (datetime.datetime.strptime(event["start_time"], '%Y-%m-%d')).strftime("%Y-%m-%d %H:%M")
        ev = FoodTruckEvents.objects.create(name=name, start_time=start_time, end_time=end_time, location=location)
        #get the event page
        event_url = 'https://graph.facebook.com/' + event["id"] + '?access_token=' + settings.FACEBOOK_ACCESS_TOKEN
        req = requests.get(event_url)
        event = req.json()
        pat = re.search(r"Vendors:\n(.*?)\n{2}", event["description"], re.DOTALL)
        if pat is not None and not pat.group(1):
            pat = re.search(r"lineup:\n(.*)\n{0,}", event["description"], re.DOTALL)

        if pat is not None:
            for food_truck in pat.group(1).split("\n"):
                if food_truck:
                    ft, state = FoodTruck.objects.get_or_create(name=food_truck)
                    ev.truck_list.add(ft)
        ev.save()
