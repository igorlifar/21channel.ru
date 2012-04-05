var currentSlide;
var sliderInterval;
var nextSlide;

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

$(document).ready(function(){
        background_color = new Array("rgb(47, 49, 56)", "rgb(40, 39, 30)", "rgb(52, 3, 54)", "rgb(16, 19, 27)", "rgb(28, 37, 38)");
        html = "";
        for(var i = 0; i < shows.length; i++){
                html += "<div class=\"slider-show\" num=\"" + i + "\">";
                html += "<img src=\"" + shows[i].image + "\">";
                html += "<div class=\"slider-show-title\" style=\"background : none repeat scroll 0% 0% " + background_color[i] + ";\">" + shows[i].title + "</div>";
                html += "</div>";
        }
        
        var set_cont = function(i) {
			$(".slider-list").html(html);
			$(".slider-content").css("background", background_color[i] + " url(" + shows[i].image + ") no-repeat");
			$(".slider-title").html(shows[i].title);
			$(".slider-schedule").html(shows[i].schedule);
			$(".slider-description").html(shows[i].description);
			$(".show-link").attr("href", "/shows/" + shows[i].id + "/")
		};
        
		set_cont(0);
		
        currentSlide = $(".slider-list").children().eq(0);
        currentSlide.children().eq(0).css("padding-left", "0px");
        currentSlide.children().eq(1).css("width", "102px");
		
		nextSlide = function(){
			var container = $(".slider-list").find("div[num=" + ((parseInt(currentSlide.attr("num")) + 1) % shows.length) + "]");
			if(container == currentSlide){
				return;
			}
			currentSlide.children().eq(0).css("padding-left", "5px");
			currentSlide.children().eq(1).css("width", "97px");
			currentSlide = container;
			currentSlide.children().eq(0).css("padding-left", "0px");
			currentSlide.children().eq(1).css("width", "102px");
			$(".slider-content").css("background", currentSlide.children().eq(1).css("background-color") + " url(" + currentSlide.children().eq(0).attr("src") + ") no-repeat"); 
			$(".slider-title").html(shows[currentSlide.attr("num")].title);
			$(".show-link").attr("href", "/shows/" + shows[currentSlide.attr("num")].id + "/")
			$(".slider-schedule").html(shows[currentSlide.attr("num")].schedule);
			$(".slider-description").html(shows[currentSlide.attr("num")].description);
		};
	
		sliderInterval = setInterval(nextSlide, 10000);
        
        $(".slider-show").mouseenter(function(){
				clearInterval(sliderInterval);
				var container = $(this);
                if(container == currentSlide){
                        return;
                }
                currentSlide.children().eq(0).css("padding-left", "5px");
                currentSlide.children().eq(1).css("width", "97px");
                currentSlide = container;
                currentSlide.children().eq(0).css("padding-left", "0px");
                currentSlide.children().eq(1).css("width", "102px");
                $(".slider-content").css("background", currentSlide.children().eq(1).css("background-color") + " url(" + currentSlide.children().eq(0).attr("src") + ") no-repeat"); 
                $(".slider-title").html(shows[currentSlide.attr("num")].title);
				$(".show-link").attr("href", "/shows/" + shows[currentSlide.attr("num")].id + "/")
                $(".slider-schedule").html(shows[currentSlide.attr("num")].schedule);
                $(".slider-description").html(shows[currentSlide.attr("num")].description);
				sliderInterval = setInterval(nextSlide, 10000);
        });
        
});