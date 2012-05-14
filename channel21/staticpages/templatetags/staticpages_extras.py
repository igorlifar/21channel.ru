from django import template

register = template.Library()

@register.filter
def pages(category):
	return category.pages.all().order_by('-priority')

@register.filter
def page_link(page):
	return '/pages/' + str(page.id) + '/'