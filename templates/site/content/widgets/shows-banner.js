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
		};
        
		set_cont(0);
		
        var current = $(".slider-list").children().eq(0);
        current.children().eq(0).css("padding-left", "0px");
        current.children().eq(1).css("width", "102px");
        
        $(".slider-show").mouseenter(function(){
                var container = $(this);
                if(container == current){
                        return;
                }
                current.children().eq(0).css("padding-left", "5px");
                current.children().eq(1).css("width", "97px");
                current = container;
                current.children().eq(0).css("padding-left", "0px");
                current.children().eq(1).css("width", "102px");
                $(".slider-content").css("background", current.children().eq(1).css("background-color") + " url(" + current.children().eq(0).attr("src") + ") no-repeat"); 
                $(".slider-title").html(shows[current.attr("num")].title);
                $(".slider-schedule").html(shows[current.attr("num")].schedule);
                $(".slider-description").html(shows[current.attr("num")].description);
        });
        
});