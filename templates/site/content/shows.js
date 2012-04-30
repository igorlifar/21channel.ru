{% if s.1 == 'list' %}
	{% include 'site/content/shows/list.js' %}
{% endif %}

{% if s.2 == 'issues' %}
	{% include 'site/content/shows/episodes.js' %}
{% endif %}

{% if s.2 == 'episodes' %}
	{% include 'site/content/shows/episodes.js' %}
{% endif %}

{% if s.2 == 'watch' %}
	{% include 'site/content/shows/watch.js' %}
{% endif %}


{% if s.1 != 'list' %}
	{% if s.2 == 'promo' or s.size == 2 %}
		{% include 'site/content/shows/show.js' %}
	{% endif %}
{% endif %}