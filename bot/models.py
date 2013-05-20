from django.db import models

# Create your models here.

#Table for all food trucks
class Food_Truck(models.Model):
	name = models.CharField(max_length=255, unique=True)
	def __unicode__(self):
		return self.name

#Table for all the events
class FoodTruckEvents(models.Model):
	name = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField(blank=True, null=True)
	truck_list = models.ManyToManyField(Food_Truck)
	def __unicode__(self):
		return self.name

