$(document).ready(function(){
	
	var size = 0;
	for(var i = 0; i < 7; i++){
		size += programs[i].length;
	}
	
	var list = new Array(size);
	
	var ptr = 0;
	
	var gettime = function(str){
		if(parseInt(str) < 10){
			return "0" + str;
		}
		return str;
	};
	
	for(var i = 0; i < 7; i++){
		for(var j = 0; j < programs[i].length; j++){
			var cur = parseInt(programs[i][j].h) * 60 + parseInt(programs[i][j].m);
			cur = cur + i * 24 * 60;
			list[ptr] = {};
			list[ptr].value = cur;
			list[ptr].time = gettime(programs[i][j].h) + ":" + gettime(programs[i][j].m);
			list[ptr].title = programs[i][j].title;
			ptr = ptr + 1;
		}
	}
	
	for(var i = 0; i < size - 1; i++){
		for(var j = i + 1; j < size; j++){
			if(parseInt(list[i].value) > parseInt(list[j].val)){
				var swp = list[i];
				list[i] = list[j];
				list[j] = swp;
			}
		}
	}
	
	var currentDate = new Date();
	var curtime = currentDate.getHours() * 60 + currentDate.getMinutes();
	curtime = curtime + ((currentDate.getDay() + 6) % 7) * 24 * 60;
	
	ptr = 0;
	
	for(var i = 0; i < list.length; i++){
		if(list.value >= curtime){
			ptr = i;
			break;
		}
	}
	
	var htmlcode = "";
	
	for(var i = 0; i < Math.min(list.length, 10); i++){
		htmlcode += "<td class=\"time\">" + list[ptr].time + "</td>";
		htmlcode += "<td class=\"show\">" + list[ptr].title + "</td>";
		ptr = (ptr + 1) % list.length;
	}
	
	$("#sch-cont").html(htmlcode);
	
	$("#sch-prev-btn").click(function(){
		$("#sch-cont").slider("moveright", "202px");
	});
	
	$("#sch-next-btn").click(function(){
		$("#sch-cont").slider("moveleft", "202px");
	});
	
	$("#video-cont").data("lock", false);
	$("#show-video-btn").click(function() {
		if($("#video-cont").data("lock")){
			return;
		}
		$("#cross-menu li").removeClass("active");
		$(this).addClass("active");
		showVideo();
	});
	
	$("#show-car-btn").click(function() {
		if($("#video-cont").data("lock")){
			return;
		}
		$("#cross-menu li").removeClass("active");
		$(this).addClass("active");
		showContent();
	})
	
	$("#show-car-btn2").click(function() {
		if($("#video-cont").data("lock")){
			return;
		}
		$("#cross-menu li").removeClass("active");
		$(this).addClass("active");
		showContent();
	})
	
} );

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

{% if s.0 == "news" %}
	{% include 'site/content/news.js' %}
{% endif %}
