from dateutil.relativedelta import relativedelta
from collections import Counter

from django.conf import settings
from bot.models import *

import requests
import datetime
import re

# gets the trucks frequency for last one month
def get_truck_frequency():
	min_date = datetime.datetime.today() - relativedelta(days=3)	
	min_date = datetime.datetime.combine(min_date, datetime.time.min)
	max_date = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)

	#get all events within the month
	event_list = FoodTruckEvents.objects.filter(start_time__range=[min_date,max_date])	
	
	total_truck_list = []
	for event in event_list:
		total_truck_list.extend([truck.name for truck in event.truck_list.all()])
			
	truck_freq = Counter(total_truck_list).most_common()
	return truck_freq 

# get trucks for today on 5th and Minna
def get_truck_list():
	date = datetime.datetime.today() 
	min_date = datetime.datetime.combine(date, datetime.time.min)
	max_date = datetime.datetime.combine(date, datetime.time.max)

	#get all events within the month
	event_list = FoodTruckEvents.objects.filter(start_time__range=[min_date,max_date])	
	
	for event in event_list:
		pat = re.search(".*(5th\sand\sMinna).*",event.location, re.DOTALL)
	
		if pat: 
			return dict(start_time=event.start_time,  
			 	truck_list = [truck.name for truck in event.truck_list.all()])
	return dict() 

# get data into database
def get_data_from_fb():
	try:
        	url = 'https://graph.facebook.com/129511477069092/events?access_token=' + settings.FACEBOOK_ACCESS_TOKEN
	        req = requests.get(url)
	        data = req.json()
		contd = data_loader(data)
	except KeyError:
		print "Access Token might have expired"
		return False

	while contd:
		try:
			url = data["paging"]
			url = url["next"] + settings.FACEBOOK_ACCESS_TOKEN
	        	req = requests.get(url)
       	 		data = req.json()
			contd = data_loader(data)
		except KeyError:
			print "Access Token might have expired"
			return False
			
#this method is used to update the database . It will only update if there is a event today
def data_loader(data):
        for event in data["data"]:
                name=event["name"]
                location=event["location"]

                try:
                        start_time = (datetime.datetime.strptime(event["start_time"][:-5],'%Y-%m-%dT%H:%M:%S')).strftime("%Y-%m-%d %H:%M")
                        if 'end_time' in event:
                                end_time = (datetime.datetime.strptime(event["end_time"][:-5],'%Y-%m-%dT%H:%M:%S')).strftime("%Y-%m-%d %H:%M")
                        else:
                                end_time = None
                except ValueError:
                        start_time = (datetime.datetime.strptime(event["start_time"],'%Y-%m-%d')).strftime("%Y-%m-%d %H:%M")

		date = datetime.datetime.today()
		min_date = datetime.datetime.combine(date, datetime.time.min)
        	max_date = datetime.datetime.combine(date, datetime.time.max)

		if min_date <= datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M') <= max_date:
                	ev = FoodTruckEvents.objects.create(name=name,start_time=start_time,end_time=end_time,location=location)
                	#get the event page
	                event_url = 'https://graph.facebook.com/' + event["id"] + '?access_token=' + settings.FACEBOOK_ACCESS_TOKEN
			try:
       	         		req = requests.get(event_url)
	                	event = req.json()
		                pat = re.search(r"Vendors:\n(.*?)\n{2}",event["description"], re.DOTALL)
		                if pat is not None and not pat.group(1):
		                        pat = re.search(r"lineup:\n(.*)\n{0,}",event["description"], re.DOTALL)

		       	        if pat is not None:
		                        for food_truck in pat.group(1).split("\n"):
		                                if food_truck:
		                                        ft, state = Food_Truck.objects.get_or_create(name=food_truck)
		                                        print ft
							ev.truck_list.add(ft)
		                ev.save()
			except KeyError:
				print "Access Token might have expired"
				return False
		elif datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M") < min_date:
			return False 
		else:
			pass
	return True 

#this method is not used anywhere
def get_initial_data():
	try:
                url = 'https://graph.facebook.com/129511477069092/events?access_token=' + settings.FACEBOOK_ACCESS_TOKEN
                req = requests.get(url)
                data = req.json()
                contd = one_time_loader(data)
        except KeyError:
                print "Access Token might have expired"
                return False

        while contd:
                try:
                        url = data["paging"]
                        url = url["next"] + settings.FACEBOOK_ACCESS_TOKEN
                        req = requests.get(url)
                        data = req.json()
                        contd = data_loader(data)
                except KeyError:
                        print "Access Token might have expired"
                        return False
	
# this method is not used  anywhere
def one_time_loader(data):
        for event in data["data"]:
                name=event["name"]
                location=event["location"]

                try:
                        start_time = (datetime.datetime.strptime(event["start_time"][:-5],'%Y-%m-%dT%H:%M:%S')).strftime("%Y-%m-%d %H:%M")
                        if 'end_time' in event:
                                end_time = (datetime.datetime.strptime(event["end_time"][:-5],'%Y-%m-%dT%H:%M:%S')).strftime("%Y-%m-%d %H:%M")
                        else:
                                end_time = None
                except ValueError:
                        start_time = (datetime.datetime.strptime(event["start_time"],'%Y-%m-%d')).strftime("%Y-%m-%d %H:%M")

		date = datetime.datetime.today() - relativedelta(month=1)
                min_date = datetime.datetime.combine(date, datetime.time.min)
                max_date = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)

                if min_date <= datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M') <= max_date:
                        ev = FoodTruckEvents.objects.create(name=name,start_time=start_time,end_time=end_time,location=location)
                        #get the event page
                        event_url = 'https://graph.facebook.com/' + event["id"] + '?access_token=' + settings.FACEBOOK_ACCESS_TOKEN
                        try:
                                req = requests.get(event_url)
                                event = req.json()
                                pat = re.search(r"Vendors:\n(.*?)\n{2}",event["description"], re.DOTALL)
                                if pat is not None and not pat.group(1):
                                        pat = re.search(r"lineup:\n(.*)\n{0,}",event["description"], re.DOTALL)

                                if pat is not None:
                                        for food_truck in pat.group(1).split("\n"):
                                                if food_truck:
                                                        ft, state = Food_Truck.objects.get_or_create(name=food_truck)
                                                        print ft
                                                        ev.truck_list.add(ft)
                                ev.save()
                        except KeyError:
                                print "Access Token might have expired"
                                return False
                elif datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M") < min_date:
                        return False
                else:
                        pass
        return True

