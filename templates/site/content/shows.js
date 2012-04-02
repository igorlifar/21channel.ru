{% if s.1 == 'list' %}
	{% include 'site/content/shows/list.js' %}
{% endif %}
{% if s.1 != 'list' and s.size == 2 %}
	{% include 'site/content/shows/show.js' %}
{% endif %}