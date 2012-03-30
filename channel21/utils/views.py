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

    
