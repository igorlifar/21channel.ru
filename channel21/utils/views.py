# Create your views here.

def evaluate_char_field(request, fieldname, maxlength, data, values, errors):
	if fieldname in request.POST:
		value = request.POST[fieldname]
		if value.strip() == "":
			values[fieldname] = ""
			errors[fieldname] = True
		else:
			if len(value) > maxlength:
				values[fieldname] = value
				errors[fieldname] = True
			else:
				values[fieldname] = value
				errors[fieldname] = False
				data[fieldname] = value
	else:
		values[fieldname] = ""
		errors[fieldname] = True

def evaluate_integer_field(request, fieldname, l, r, data, values, errors):
	if fieldname in request.POST:
		try:
			value = int(request.POST[fieldname])
			if value < l or value > r:
				values[fieldname] = ""
				errors[fieldname] = True
			else:
				data[fieldname] = value
				values[fieldname] = value
				errors[fieldname] = False
		except:
			values[fieldname] = ""
			errors[fieldname] = True
	else:
		values[fieldname] = ""
		errors[fieldname] = True
