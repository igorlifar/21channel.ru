from news.models import *
from utils.views import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from urllib import quote, unquote

# Create your views here.

def create_news_item(request):
	try:
		values = {}
		errors = {}
		data = {}
		evaluate_char_field(request, "title", 1000, data, values, errors)
		evaluate_char_field(request, "preview", 1000, data, values, errors)
		evaluate_char_field(request, "text", 10000, data, values, errors)
		errors["image"] = False
		values["image_change"] = "no"
		if "image_change" in request.POST:
			values["image_change"] = request.POST["image_change"]
		if len(data) == 3:
			newItem = NewsItem.objects.create(title = data["title"], preview = data["preview"], text = data["text"])
			if "image" in request.FILES:
				values["image_change"] = "image"
				try:
					newItem.load_image(request.FILES["image"])
				except:
					newItem.delete()
					errors["image"] = True
					return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
			return redirect(request.POST["redirect_good_url"])
		else:
			return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
	except:
		return redirect("/")

def delete_news_item(request):
	try:
		if "id" in request.POST:
			newsid = int(request.POST["id"])
			items = NewsItem.objects.filter(id = newsid)
			if items.count() != 0:
				item = items[0]
				if item.image.__nonzero__():
					item.image.delete()
				item.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		
def update_news_item(request):
	try:
		if "newsid" in request.POST:
			newsid = int(request.POST["newsid"])
			items = NewsItem.objects.filter(id = newsid)
			if items.count() != 0:
				item = items[0]
				values = {}
				errors = {}
				data = {}
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "preview", 1000, data, values, errors)
				evaluate_char_field(request, "text", 10000, data, values, errors)
				errors["new_image"] = False
				values["image_change"] = "no"
				if "image_change" in request.POST:
					values["image_change"] = request.POST["image_change"]
				if len(data) == 3:
					item.title = data["title"]
					item.preview = data["preview"]
					item.text = data["text"]
					item.save()
					if "image_change" in request.POST:
						image_change = request.POST["image_change"]
						values["image_change"] = image_change
						if image_change == "delete" and item.image.__nonzero__():
							item.image.delete()
						if image_change == "new_image" and "new_image" in request.FILES:
							try:
								item.load_image(request.FILES["new_image"])
							except:
								errors["new_image"] = True
								return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
					return redirect(request.POST["redirect_good_url"] + "?success")
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"newsid" : True}})))
	except:
		return redirect("/")