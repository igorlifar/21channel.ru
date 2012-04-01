$(document).ready(function(){
	
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