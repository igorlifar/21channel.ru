$(document).ready(function(){
        
        background_color = new Array("rgb(47, 49, 56)", "rgb(40, 39, 30)", "rgb(52, 3, 54)", "rgb(16, 19, 27)", "rgb(28, 37, 38)");
        html = "";
        for(var i = 0; i < shows.length; i++){
                html += "<div class=\"slider-show\" num=\"" + i + "\">";
                html += "<img src=\"" + shows[i].image + "\">";
                html += "<div class=\"slider-show-title\" style=\"background : none repeat scroll 0% 0% " + background_color[i] + ";\">" + shows[i].title + "</div>";
                html += "</div>";
        }
        
        $(".slider-list").html(html);
        $(".slider-image").css("background", "url(" + shows[0].image + ") no-repeat");
        $(".slider-text").css("background", "none repeat scroll 0% 0% " + background_color[0]);
        $(".slider-title").html(shows[0].title);
        $(".slider-schedule").html(shows[0].schedule);
        $(".slider-description").html(shows[0].description);
        
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
                $(".slider-image").css("background", "url(" + current.children().eq(0).attr("src") + ") no-repeat");
                $(".slider-text").css("background", "none repeat scroll 0% 0% " + current.children().eq(1).css("background-color")); 
                $(".slider-title").html(shows[current.attr("num")].title);
                $(".slider-schedule").html(shows[current.attr("num")].schedule);
                $(".slider-description").html(shows[current.attr("num")].description);
        });
        
});