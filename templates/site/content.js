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

function showVideo(){
	if($("#video-cont").data("lock")){
		return;
	}
	$("#video-cont").data("lock", true);
	$("#video-car").animate({
		opacity : 0
	}, "slow", function(){
		$("#video-car").css("display", "none");
		loadVideo($("#video-vid"));
		$("#video-cont").data("lock", false);
	});
}

function showContent(){
	if($("#video-cont").data("lock")){
		return;
	}
	$("#video-cont").data("lock", true);
	loadContainer($("#video-vid"), "", function(){
		$("#video-car").css("display", "block");
		$("#video-car").animate({
			opacity : 1
		}, "slow", function(){
			$("#video-cont").data("lock", false);
		});
	});
}

var settings = {
	urlPlayer : "/static_files/flowplayer/flowplayer-3.2.8.swf",
	urlPlayerRTMP : "/static_files/flowplayer/flowplayer.rtmp-3.2.8.swf",
	streams : [{url : "plus500"}, {url : "plus1000"}],
	connectionUrl : "rtmp://83.229.210.89/PLUS21",
	imgButton : "/static_files/flowplayer/showme.png"
};

function loadContainer(container, content, callback){
	container.animate({
		opacity : 0	
	}, "slow", function(){
		if(container.data("video") == "playing"){
	  		$f("streams", settings.urlPlayer);
			container.data("video", "");
		}
		container.html(content);
		callback();
	});
}

function loadVideo(container){
	container.data("video", "playing");
	container.animate({
		opacity : 0
	}, "fast", function(){
		container.html('<div class="box black"><a class="player" id="streams"><img class="button" src="' + settings.imgButton + '"></a></div>');
		$f("streams", settings.urlPlayer, {
    	clip : {
        provider : 'influxis',
        streams : settings.streams
    	},
 			plugins : {
        influxis : {
            url : settings.urlPlayerRTMP,
            netConnectionUrl : settings.connectionUrl
        }
    	}
		});
		container.animate({
			opacity : 1
		}, "fast");
	});
}