from django import template

register = template.Library()

@register.filter
def screenshot(value):
	return value.video.get_screen_shot()

@register.filter
def player(value, arg):
	dim = arg.split('x')
	
	return value.video.get_player(dim[0], dim[1])
	
@register.filter
def link(value):
	if not value.show == None:
		return "/shows/" + str(value.show.id) + "/watch/" + str(value.id) + "/"
	else:
		return "/episode/" + str(value.id) + "/"