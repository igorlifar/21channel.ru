from django import template

register = template.Library()

@register.filter
def paragraphize(value):
	a = value.replace('\n\r', '\n').split('\n\n')
	b = []
	for i in a:
		if not i == '':
			b.append(i)
			
	return b
	