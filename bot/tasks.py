from dateutil.relativedelta import relativedelta
from celery.schedules import *
from celery.task import periodic_task
from celery import task

from django_hipchat.api import hipchat_message
from bot.trucks import get_truck_list, get_data_from_fb


@task
def check_send_food_info():
    """celery task for checking the truck list"""
    try:
        truck_list = get_truck_list()
        hipchat_message("chat_message.html", {'trucks': truck_list})
    except Exception, e:
        print e


@task
def update_database():
    get_data_from_fb()
    truck_list = get_truck_list()

    if truck_list:
        post_time = truck_list["start_time"] - relativedelta(minutes=30)
        check_send_food_info.apply_async(eta=post_time)
