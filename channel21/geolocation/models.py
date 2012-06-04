from django.db import models
from django_geoip.models import *

# Create your models here.

class geoLocation(GeoLocationFacade):
	
	region = models.OneToOneField(Region, related_name = "geo_location")
	is_default = models.BooleanField(default = False)
	
	@classmethod
	def get_by_ip_range(cls, ip_range):
		try:
			return ip_range.region.geo_location
		except:
			raise IpRange.DoesNotExist
		
	@classmethod
	def get_default_location(cls):
		return cls.objects.get(is_default = True)
		
	@classmethod
	def get_available_locations(cls):
		return cls.objects.all()
		
	class Meta:
		db_table = "geo_location"
		