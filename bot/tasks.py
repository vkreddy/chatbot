from dateutil.relativedelta import relativedelta
from celery.schedules import * 
from celery.task import periodic_task
from celery import task

from django_hipchat.api import hipchat_message
from bot.trucks import *

from datetime import * 

@task
def CheckSendFoodInfo():
	try:
		truck_list = get_truck_list()
		hipchat_message("chat_message.html", {'trucks': truck_list})	
	except Exception, e:
		print e


# set the time in settings.py 
@task
def update_database():
	get_data_from_fb()
	truck_list = get_truck_list()
	if truck_list:
		post_time = truck_list["start_time"] - retativedelta(minutes=30)	
		CheckSendFoodInfo.apply_async(eta=post_time)
