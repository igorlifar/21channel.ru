from django.http import Http404

def parse_path(request):
	path = request.path.replace('site', 'index').replace('.css', '').replace('-', '/').strip('/').split('/')
	return path[1:len(path)+1]

def get_panel_section(request):
	path = parse_path(request)
	
	print path
	
	if len(path) > 0 and path[0] == 'panel':
		if len(path) == 1:
			return ["index"]
		else:
			raise Http404
	else:
		raise Http404
	
def get_site_section(request):
	path = parse_path(request)
	
	return path