from django.http import Http404

def get_panel_section(request):
	path = request.path.strip('/').split('/')
	
	if len(path) > 0 and path[0] == 'panel':
		if len(path) == 1:
			return ["index"]
		else:
			raise Http404
	else:
		raise Http404
	
def get_site_section(request):
	path = request.path.strip('/').split('/')
	
	level1 = ["shows", "archive", "episode", "schedule"]
	
	if len(path) == 0 or not path[0] in a:
		path.insert(0, "index")
		
	if path[0] == "index":
		if len(path) == 1:
			return ["index"]
		else:
			raise Http404
	else:
		raise Http404