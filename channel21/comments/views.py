from comments.models import ShowComment
from shows.models import Show
from django.shortcuts import redirect



# Create your views here.


def create_show_comment(request):
	redirect_url = '/'
	try:
		redirect_url = request.POST["redirect_url"]
	except:
		pass
	
	try:
		body = request.POST["body"]
		
		if len(body) == 0 or len(body) > 10000:
			raise ValueError("invalid body")
		
		author = request.user
		if not author.is_active:
			raise ValueError("invalid user")
		
		print request.POST
		
		show = Show.objects.get(id=int(request.POST['show']))
		
		print 5
		
		ShowComment.objects.create(body = body, author = author, show = show)
		
	except:
		pass
	
	return redirect(redirect_url)
		