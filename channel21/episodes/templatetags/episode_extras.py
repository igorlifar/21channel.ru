from django import template

register = template.Library()

@register.filter
def screenshot(episode):
	return episode.get_screenshot()

@register.filter
def player(episode, arg):
	dim = arg.split('x')
	
	return episode.get_video().get_player(dim[0], dim[1])
	
@register.filter
def link(episode):
	return episode.get_link()

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