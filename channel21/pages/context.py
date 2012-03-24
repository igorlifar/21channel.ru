def get_panel_context(section, request):
	res = {}
	
	if len(section) > 0:
		if section[0] == "login-page":
			res.update({"redirect_url": request.path})
			
	return res
	
def get_site_context(section, request):
	res = {}
	
	return res