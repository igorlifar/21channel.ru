from django import template

register = template.Library()

@register.filter
def profile_title(user):
	return user.first_name + u' ' + user.last_name
    
@register.filter
def profile_ulogin(user):
	try:
		return user.ulogin_users.all()[0]
	except:
		return None
		
@register.filter
def ulogin_identity(ulogin):
	return ulogin.identity
	
@register.filter
def datetime(date):
	return date.strftime("%d.%m.%Y %H:%M")