from geolocation.models import *
from django_geoip.models import *
from django.shortcuts import redirect, render_to_response
from urllib import quote, unquote
import json
from mainsettings.models import LocalSettings
from schedule.models import Program

# Create your views here.

def add_location(request):
	
	try:
		values = {}
		errors = {}
		if "regionid" in request.POST:
			try:
				values["regionid"] = int(request.POST["regionid"])
				errors["regionid"] = False
			except:
				values["regionid"] = ""
				errors["regionid"] = True
			if not errors["regionid"]:
				regions = Region.objects.filter(id = values["regionid"])
				if regions.count() != 0:
					region = regions[0]
					if geoLocation.objects.filter(region = region).count() == 0:
						location = geoLocation.objects.create(region = region)
						localsettings = LocalSettings.objects.create(region = location)
						return redirect(request.POST["redirect_good_url"])
			errors["regionid"] = True
		else:
			values["regionid"] = ""
			errors["regionid"] = True
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
	except:
		return redirect("/")
		
		
def delete_location(request):
	
	try:
		if "regionid" in request.POST:
			regionid = int(request.POST["regionid"])
			regions = geoLocation.objects.filter(id = regionid)
			if regions.count() != 0:
				region = regions[0]
				localsettings = LocalSettings.objects.get(region = region)
				localsettings.delete()
				region.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		