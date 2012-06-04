from django.db import models
from geolocation.models import geoLocation

# Create your models here.

class Program(models.Model):
	
	title = models.CharField(max_length = 1000, blank = True)
	description = models.CharField(max_length = 10000, blank = True)
	dayofweek = models.IntegerField(blank = True, null = True)
	starttime = models.CharField(max_length = 100, blank = True)
	finishtime = models.CharField(max_length = 100, blank = True)
	region = models.ForeignKey(geoLocation, related_name = "for region", blank = True, null = True)
	