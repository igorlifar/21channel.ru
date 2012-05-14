from staticpages.models import *
from utils.views import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from urllib import quote, unquote

# Create your views here.

def create_page(request):
	try:
		values = {}
		errors = {}
		data = {}
		evaluate_char_field(request, "title", 1000, data, values, errors)
		evaluate_char_field(request, "body", 10000, data, values, errors)
		if "category" in request.POST:
			categoryid = int(request.POST["category"])
			categories = Category.objects.filter(id = categoryid)
			if categories.count() != 0:
				data["category"] = categories[0]
				values["category"] = categoryid
				errors["category"] = False
			else:
				values["category"] = ""
				errors["category"] = True
		else:
			values["category"] = ""
			errors["category"] = True
		if "priority" in request.POST:
			try:
				values["priority"] = int(request.POST["priority"])
				data["priority"] = values["priority"]
				errors["priority"] = False
			except:
				values["priority"] = ""
				errors["priority"] = True
		else:
			values["priority"] = ""
			errors["priority"] = True
		if len(data) == 4:
			newpage = Page.objects.create(title = data["title"], body = data["body"], category = data["category"], priority = data["priority"])
			return redirect(request.POST["redirect_good_url"])
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
	except:
		return redirect("/")
		
def update_page(request):
	try:
		if "pageid" in request.POST:
			pageid = int(request.POST["pageid"])
			pages = Page.objects.filter(id = pageid)
			if pages.count() != 0:
				page = pages[0]
				values = {}
				errors = {}
				data = {}
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "body", 10000, data, values, errors)
				if "category" in request.POST:
					categoryid = int(request.POST["category"])
					categories = Category.objects.filter(id = categoryid)
					if categories.count() != 0:
						data["category"] = categories[0]
						values["category"] = categoryid
						errors["category"] = False
					else:
						values["category"] = ""
						errors["category"] = True
				else:
					values["category"] = ""
					errors["category"] = True
				if "priority" in request.POST:
					try:
						values["priority"] = int(request.POST["priority"])
						data["priority"] = values["priority"]
						errors["priority"] = False
					except:
						values["priority"] = ""
						errors["priority"] = True
				else:
					values["priority"] = ""
					errors["priority"] = True
				if len(data) == 4:
					page.title = data["title"]
					page.body = data["body"]
					page.category = data["category"]
					page.priority = data["priority"]
					page.save()
					return redirect(request.POST["redirect_good_url"] + "?success")
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"pageid" : True}})))
	except:
		return redirect("/")
		
def delete_page(request):
	try:
		if "pageid" in request.POST:
			pageid = int(request.POST["pageid"])
			pages = Page.objects.filter(id = pageid)
			if pages.count() != 0:
				page = pages[0]
				page.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")