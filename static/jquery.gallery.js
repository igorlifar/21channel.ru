(function($){
	
	var settings = {
		width : "500px",
		height : "400px"
	};
	
	var methods = {
		init : function(overrideSettings){
			settings = $.extend(settings, overrideSettings);
		},
		show : function(gallery){
			if(typeof(gallery.shift) == "undefined"){
				gallery.shift = 0;
			}
			$(document).data("gallery-container", $(this));
			$(document).data("gallery-urls", gallery.urls);
			$(document).data("gallery-shift", gallery.shift);
			var style = "margin-left : " + Math.max(Math.floor((parseInt($(window).width()) - parseInt(settings.width)) / 2), 0) + "px;";
			style += "margin-top : " + Math.max(Math.floor((parseInt($(window).height()) - parseInt(settings.height)) / 2), 0) + "px;";
			style += "width : " + settings.width + ";";
			style += "height : " + settings.height + ";";
			var html = "<div class=\"gallery-background\" onclick=\"$(document).gallery('close');\"></div>";
			html += "<div class=\"gallery-body\" style=\"" + style + "\">";
			html += "<div class=\"gallery-header\"><div class=\"gallery-current-shot\">Кадр " + (parseInt(gallery.shift) + 1) + " из " + gallery.urls.length + "</div>";
			html += "<div class=\"gallery-close\" onclick=\"$(document).gallery('close');\">Закрыть</div></div>";
			html += "<div class=\"gallery-image\"><img onclick=\"$(document).gallery('nextimage');\" src=\"" + gallery.urls[gallery.shift] + "\"></div>";
			html += "</div>";
			$(this).html(html);
		},
		close : function(){
			var container = $(document).data("gallery-container");
			container.html("");
		},
		nextimage : function(){
			var urls = $(document).data("gallery-urls");
			var shift = $(document).data("gallery-shift");
			shift = (parseInt(shift) + 1) % urls.length;
			$(document).data("gallery-shift", shift);
			$(".gallery-current-shot").html("Кадр " + (shift + 1) + " из " + urls.length);
			$(".gallery-image img").attr("src", urls[shift]);
		}
	};
	
	$.fn.gallery = function(method){
		if(methods[method]){
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		}
		else{
			if(typeof(method) === "object" || typeof(method) === "undefined"){
				return methods.init.apply(this, arguments);
			}
			else{
				console.log("gallery: method \"" + method + "\" does not exist");
			}
		}
	}
	
})(jQuery);