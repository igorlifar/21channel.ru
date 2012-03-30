def get_panel_context(section, request):
	res = {
		"static": "/static_files/"
	}
	
	if request.user.is_anonymous():
		res["user"] = {
			"anonymous": True
		}
	else:
		res["user"] = {
			'anonymous': False,
			'name': request.user.first_name + ' ' + request.user.last_name
		}
			
			
	return res
	
def get_site_context(section, request):
	res = {}
	
	return res