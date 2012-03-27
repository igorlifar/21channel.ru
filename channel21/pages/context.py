def get_panel_context(section, request):
	res = {
		"static": "/static_files/"
	}
	
	if len(section) > 0:
		if section[0] == "login-page":
			res.update({"redirect_url": request.path})
			
		if section[0] == "index":
			res.update({"css": "panel.css"})
			
	return res
	
def get_site_context(section, request):
	res = {}
	
	return res