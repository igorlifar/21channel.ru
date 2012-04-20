from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout


def login_panel(request):
	try:
		username = request.POST['login']
		password = request.POST['password']
		
		print username
		print password
		
		user = authenticate(username=username, password=password)

		if user is not None and user.is_active:
			login(request, user)
			return redirect("/panel/")
		else:
			return redirect("/panel/login/?wrongdata=1")
	except:
		return redirect("/panel/login/?wrongdata=1")
		
def logout_site(request):
	logout(request)
	
	try:
		return redirect(request.POST['redirect_url'])
	except:
		return redirect("/")
		
def logout_panel(request):
	logout(request)
	return redirect("/panel/login/")