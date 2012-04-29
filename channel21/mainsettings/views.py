from shows.models import *
from mainsettings.models import *
from utils.views import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from urllib import quote, unquote

# Create your views here.

def update_settings(request):
	try:
		mainsettings = MainSettings.objects.all()[0]
		values = {}
		errors = {}
		data = {}
		errors["showid1"] = False
		if "showid1" in request.POST:
			try:
				showid = int(request.POST["showid1"])
				if showid == -1:
					data["showid1"] = None
				else:
					shows = Show.objects.filter(id = showid)
					if shows.count() != 0:
						data["showid1"] = shows[0]
				errors["showid1"] = False
			except:
				errors["showid1"] = True
		errors["showid2"] = False
		if "showid2" in request.POST:
			try:
				showid = int(request.POST["showid2"])
				if showid == -1:
					data["showid2"] = None
				else:
					shows = Show.objects.filter(id = showid)
					if shows.count() != 0:
						data["showid2"] = shows[0]
				errors["showid2"] = False
			except:
				errors["showid2"] = True
		errors["showid3"] = False
		if "showid3" in request.POST:
			try:
				showid = int(request.POST["showid3"])
				if showid == -1:
					data["showid3"] = None
				else:
					shows = Show.objects.filter(id = showid)
					if shows.count() != 0:
						data["showid3"] = shows[0]
				errors["showid3"] = False
			except:
				errors["showid3"] = True
		errors["showid4"] = False
		if "showid4" in request.POST:
			try:
				showid = int(request.POST["showid4"])
				if showid == -1:
					data["showid4"] = None
				else:
					shows = Show.objects.filter(id = showid)
					if shows.count() != 0:
						data["showid4"] = shows[0]
				errors["showid4"] = False
			except:
				errors["showid4"] = True
		errors["showid5"] = False
		if "showid5" in request.POST:
			try:
				showid = int(request.POST["showid5"])
				if showid == -1:
					data["showid5"] = None
				else:
					shows = Show.objects.filter(id = showid)
					if shows.count() != 0:
						data["showid5"] = shows[0]
				errors["showid5"] = False
			except:
				errors["showid5"] = True
		values["background_change"] = "no"
		errors["new_background"] = False
		if "background_change" in request.POST:
			background_change = request.POST["background_change"]
			values["background_change"] = background_change
			if background_change == "delete" and mainsettings.background.__nonzero__():
				mainsettings.background.delete()
			if background_change == "new_background":
				if "new_background" in request.FILES:
					try:
						mainsettings.load_image(request.FILES["new_background"])
					except:
						errors["new_background"] = True
						return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
				else:
					errors["new_background"] = True
					return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		if "showid1" in data:
			mainsettings.show1 = data["showid1"]
		if "showid2" in data:
			mainsettings.show2 = data["showid2"]
		if "showid3" in data:
			mainsettings.show3 = data["showid3"]
		if "showid4" in data:
			mainsettings.show4 = data["showid4"]
		if "showid5" in data:
			mainsettings.show5 = data["showid5"]
		mainsettings.save()
		return redirect(request.POST["redirect_good_url"] + "?success")
	except:
		return redirect("/")