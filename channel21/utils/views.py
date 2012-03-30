# Create your views here.

def evaluate_char_field(request, fieldname, maxlength, data, values, errors):
	if fieldname in request.POST:
		value = request.POST[fieldname]
		if value.strip() == "":
			values.append({fieldname : ""})
			errors.append(fieldname)
		else:
			if len(value) > maxlength:
				values.append({fieldname : value})
				errors.append(fieldname)
			else:
				values.append({fieldname : value})
				data[fieldname] = value
	else:
		values.append({fieldname : ""})
		errors.append(fieldname)

    
