$(document).ready(function(){
	
	$(".video-site .vd").each(function(){
		fillContainer($(this), $(this).parent().find("input").val(), "200px", "120px");
	});
	
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
		if(programs[i].length == 0){
			$("#day" + i).append("<li style=\"width : " + (24 * 60 * 4 - 1) + "px;\"></li>");
			continue;
		}
		var sz = 0;
		var lst = new Array(programs[i].length);
		for(var j = 0; j < programs[i].length; j++){
			var cur = parseInt(programs[i][j].h) * 60 + parseInt(programs[i][j].m);
			lst[sz] = {};
			lst[sz].value = cur;
			lst[sz].len = parseInt(programs[i][j].len)
			lst[sz].time = gettime(programs[i][j].h) + ":" + gettime(programs[i][j].m);
			lst[sz].title = programs[i][j].title;
			sz = sz + 1; 
		}
		for(var j = 0; j < sz - 1; j++){
			for(var z = j + 1; z < sz; z++){
				if(lst[j].value > lst[z].value){
					var swp = lst[j];
					lst[j] = lst[z];
					lst[z] = swp;
				}
			}
		}
		var schedulecode = "";
		var cur = 0;
		for(var j = 0; j < sz; j++){
			if(lst[j].value >= 5 * 60){
				cur = j;
				break;
			}
		}
		var last = 5 * 60;
		for(var j = 0; j < sz; j++){
			if(lst[cur].value < last){
				lst[cur].value = lst[cur].value + 24 * 60;
			}
			if(lst[cur].value != last){
				schedulecode += "<li class=\"empty\" style=\"width : " + ((lst[cur].value - last) * 4 - 1) + "px;\">-</li>";
			}
			schedulecode += "<li style=\"width : " + (lst[cur].len * 4 - 1) + "px;\">" + lst[cur].title + "</li>";
			last = lst[cur].value + lst[cur].len;
			cur = (cur + 1) % sz;
		}
		if(last != 29 * 60){
			schedulecode += "<li style=\"width : " + ((29 * 60 - last) * 4 - 1) + "px;\"></li>";
		}
		$("#day" + i).append(schedulecode);
	}
	
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
			if(parseInt(list[i].value) > parseInt(list[j].value)){
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
		if(list[i].value >= curtime){
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
	
	$(".video-site .next-btn").click(function() {
		$(this).parent().find(".cont").slider("moveleft", "225px");
	});
	
	$(".video-site .prev-btn").click(function() {
		$(this).parent().find(".cont").slider("moveright", "225px");
	});
	
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

console.log("12sadasdasd");

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
