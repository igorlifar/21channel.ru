from django import template

register = template.Library()

@register.filter
def screenshot(value):
	return value.video.get_screen_shot()

@register.filter
def player(value, arg):
	dim = arg.split('x')
	
	return value.video.get_player(dim[0], dim[1])