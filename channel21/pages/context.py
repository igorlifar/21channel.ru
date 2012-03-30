from news.models import NewsItem

def get_panel_context(s, request):
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
		
	if len(s) >= 1:
		if s[0] == 'news':
			if len(s) >= 2:
				if s[1] == 'list':
					res["news"] = NewsItem.objects.all()
			
			
	return res
	
def get_site_context(section, request):
	res = {}
	
	return res