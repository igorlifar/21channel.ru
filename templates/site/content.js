{% include 'site/content/widgets/shows-banner.js' %}

{% if s.0 == "index" %}
	{% include 'site/content/index.js' %}
{% endif %}

{% if s.0 == "shows" %}
	{% include 'site/content/shows.js' %}
{% endif %}

{% if s.0 == "archive" %}
	{% include 'site/content/archive.js' %}
{% endif %}

{% if s.0 == "schedule" %}
	{% include 'site/content/schedule.js' %}
{% endif %}

{% if s.0 == "coverage" %}
	{% include 'site/content/coverage.js' %}
{% endif %}