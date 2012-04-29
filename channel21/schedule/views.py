from django.shortcuts import redirect
from schedule.models import *
from utils.views import *
import json
from urllib import quote

# Create your views here.

def create_program(request):
	try:
		values = {}
		errors = {}
		data = {}
		evaluate_integer_field(request, "dayofweek", 0, 6, data, values, errors)
		evaluate_char_field(request, "title", 1000, data, values, errors)
		evaluate_char_field(request, "description", 10000, data, values, errors)
		evaluate_char_field(request, "starttime", 100, data, values, errors)
		evaluate_char_field(request, "finishtime", 100, data, values, errors)
		if len(data) == 5:
			time1 = data["starttime"].split(":")
			if len(time1) != 2:
				errors["starttime"] = True
			time2 = data["finishtime"].split(":")
			if len(time2) != 2:
				errors["finishtime"] = True
			if len(time1) == 2 and len(time2) == 2:
				bad = False
				try:
					h1 = int(time1[0])
					m1 = int(time1[1])
					h2 = int(time2[0])
					m2 = int(time2[1])
				except:
					bad = True
					h1 = 0
					m1 = 0
					h2 = 0
					m2 = 0
				val1 = h1 * 60 + m1
				val2 = h2 * 60 + m2
				if val1 > val2:
					val2 = val2 + 24 * 60
				for t in range(val1 + 1, val2):
					if t == 5 * 60 or t == 29 * 60:
						bad = True
				if bad:
					errors["starttime"] = True
					errors["finishtime"] = True
				else:
					for program in Program.objects.filter(dayofweek = data["dayofweek"]):
						time3 = program.starttime.split(":")
						time4 = program.finishtime.split(":")
						h3 = int(time3[0])
						m3 = int(time3[1])
						h4 = int(time4[0])
						m4 = int(time4[1])
						val3 = h3 * 60 + m3
						val4 = h4 * 60 + m4
						if val3 > val4:
							val4 = val4 + 24 * 60
						l = max(val1, val3)
						r = min(val2, val4)
						if l < r:
							bad = True
					if bad:
						errors["starttime"] = True
						errors["finishtime"] = True
					else:
						newprogram = Program.objects.create(title = data["title"], description = data["description"], dayofweek = data["dayofweek"], starttime = data["starttime"], finishtime = data["finishtime"])
						return redirect(request.POST["redirect_good_url"])
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
	except:
		return redirect("/")
		
def delete_program(request):
	try:
		if "programid" in request.POST:
			programid = int(request.POST["programid"])
			programs = Program.objects.filter(id = programid)
			if programs.count() != 0:
				program = programs[0]
				program.delete()
		return redirect(request.POST["redirect_url"])
	except:
		return redirect("/")
		
def update_program(request):
	try:
		if "programid" in request.POST:
			programid = int(request.POST["programid"])
			programs = Program.objects.filter(id = programid)
			if programs.count() != 0:
				program = programs[0]
				values = {}
				errors = {}
				data = {}
				evaluate_integer_field(request, "dayofweek", 0, 6, data, values, errors)
				evaluate_char_field(request, "title", 1000, data, values, errors)
				evaluate_char_field(request, "description", 10000, data, values, errors)
				evaluate_char_field(request, "starttime", 100, data, values, errors)
				evaluate_char_field(request, "finishtime", 100, data, values, errors)
				if len(data) == 5:
					time1 = data["starttime"].split(":")
					if len(time1) != 2:
						errors["starttime"] = True
					time2 = data["finishtime"].split(":")
					if len(time2) != 2:
						errors["finishtime"] = True
					if len(time1) == 2 and len(time2) == 2:
						bad = False
						try:
							h1 = int(time1[0])
							m1 = int(time1[1])
							h2 = int(time2[0])
							m2 = int(time2[1])
						except:
							bad = True
							h1 = 0
							m1 = 0
							h2 = 0
							m2 = 0
						val1 = h1 * 60 + m1
						val2 = h2 * 60 + m2
						if val1 > val2:
							val2 = val2 + 24 * 60
						for t in range(val1 + 1, val2):
							if t == 5 * 60 or t == 29 * 60:
								bad = True
						if bad:
							errors["starttime"] = True
							errors["finishtime"] = True
						else:
							for cprogram in Program.objects.filter(dayofweek = data["dayofweek"]):
								if cprogram.id != program.id:
									time3 = program.starttime.split(":")
									time4 = program.finishtime.split(":")
									h3 = int(time3[0])
									m3 = int(time3[1])
									h4 = int(time4[0])
									m4 = int(time4[1])
									val3 = h3 * 60 + m3
									val4 = h4 * 60 + m4
									if val3 > val4:
										val4 = val4 + 24 * 60
									l = max(val1, val3)
									r = min(val2, val4)
									if l < r:
										bad = True
							if bad:
								errors["starttime"] = True
								errors["finishtime"] = True
							else:
								program.title = data["title"]
								program.description = data["description"]
								program.starttime = data["starttime"]
								program.finishtime = data["finishtime"]
								program.dayofweek = data["dayofweek"]
								program.save()
								return redirect(request.POST["redirect_good_url"] + "?success")
				return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : values, "errors" : errors})))
		return redirect(request.POST["redirect_bad_url"] + "?formstate=" + quote(json.dumps({"values" : {}, "errors" : {"programid" : True}})))
	except:
		return redirect("/")	