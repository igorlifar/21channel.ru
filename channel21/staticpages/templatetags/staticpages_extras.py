from django import template

register = template.Library()

@register.filter
def pages(category):
	return category.pages.all().order_by('-priority')