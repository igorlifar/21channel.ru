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
		if value.episodetype == 'I':
			return "/shows/" + str(value.show.id) + "/issues/watch/" + str(value.id) + "/"
		if value.episodetype == 'E':
			return "/shows/" + str(value.show.id) + "/episodes/watch/" + str(value.id) + "/"
		return "/shows/" + str(value.show.id) + "/promo/watch/" + str(value.id) + "/"
	else:
		return "/episode/" + str(value.id) + "/"

@register.filter
def backlink(value):
	if not value.show == None:
		if value.episodetype == 'I':
			return "/shows/" + str(value.show.id) + "/issues/"
		if value.episodetype == 'E':
			return "/shows/" + str(value.show.id) + "/episodes/"
		if value.episodetype == 'P':
			return "/shows/" + str(value.show.id) + "/"
	return "/"