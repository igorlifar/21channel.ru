(function($){
	
	var settings = {
		width : "200px",
		height : "200px",
		widthScroll : "20px",
		heightScroll : "20px"
	};
	
	var methods = {
		init : function(overrideSettings){
			if(typeof(overrideSettings) != "undefined"){
				settings = $.extend(settings, overrideSettings);
			}
			return this.each(function(){
				var container = $(this);
				var html = container.html();
				container.css("position", "relative");
				container.css("overflow", "hidden");
				container.css("height", settings.height);
				container.html("<div class=\"scroll-body\" style=\"position : absolute; width : " + (parseInt(settings.width) - parseInt(settings.widthScroll)) + "px; margin-right : " + settings.widthScroll + ";\">" + html + "</div><div class=\"scroll-column\" style=\"position : absolute; right : 0px; width : " + settings.widthScroll + "; height : " + settings.height + ";\"><div class=\"scroll-up\">&nbsp;</div><div class=\"scroll-go\" style=\"position : relative;\"><div style=\"position : absolute; width : " + settings.widthScroll + "; height : " + settings.heightScroll + ";\" class=\"scroll-control\">&nbsp;</div></div><div class=\"scroll-down\">&nbsp;</div></div>");
				container.children().eq(1).children().eq(1).css("height", parseInt(settings.height) - 2 * $(".scroll-up").outerHeight());
				container.data("active", false);
				container.children().eq(1).children().eq(1).children().eq(0).mousedown(function(){
					$(this).data("active", true);
				});
				container.children().eq(1).children().eq(1).children().eq(0).mouseup(function(){
					$(this).data("active", false);
				});
				container.children().eq(1).children().eq(1).mousemove(function(cursor){
					var scroll = $(this).children().eq(0);
					if(!scroll.data("active")){
						return;
					}
					var y = cursor.pageY - $(this).offset().top - Math.floor(parseInt(settings.heightScroll) / 2);
					y = Math.max(y, 0);
					y = Math.min(y, parseInt(settings.height) - 2 * $(".scroll-up").outerHeight() - parseInt(settings.heightScroll));
					scroll.css("margin-top", y);
					var percent = y / (parseInt(settings.height) - 2 * $(".scroll-up").outerHeight() - parseInt(settings.heightScroll));
					var container = $(this).parent().parent().children().eq(0);
					container.css("margin-top", -Math.floor(percent * Math.max(container.outerHeight() - parseInt(settings.height), 0)));
				});
				container.children().eq(1).children().eq(2).click(function(){
					var container = $(this).parent().parent().children().eq(0);
					var y = parseInt($(this).parent().children().eq(1).children().eq(0).css("margin-top"));
					var percent = y / (parseInt(settings.height) - 2 * $(".scroll-up").outerHeight() - parseInt(settings.heightScroll));
					percent = Math.min(percent + 0.1, 1);
					container.css("margin-top", -Math.floor(percent * Math.max(container.outerHeight() - parseInt(settings.height), 0)));
					$(this).parent().children().eq(1).children().eq(0).css("margin-top", Math.floor(percent * (parseInt(settings.height) - 2 * $(".scroll-up").outerHeight() - parseInt(settings.heightScroll))));
				});
				container.children().eq(1).children().eq(0).click(function(){
					var container = $(this).parent().parent().children().eq(0);
					var y = parseInt($(this).parent().children().eq(1).children().eq(0).css("margin-top"));
					var percent = y / (parseInt(settings.height) - 2 * $(".scroll-up").outerHeight() - parseInt(settings.heightScroll));
					percent = Math.max(percent - 0.1, 0);
					container.css("margin-top", -Math.floor(percent * Math.max(container.outerHeight() - parseInt(settings.height), 0)));
					$(this).parent().children().eq(1).children().eq(0).css("margin-top", Math.floor(percent * (parseInt(settings.height) - 2 * $(".scroll-up").outerHeight() - parseInt(settings.heightScroll))));
				});
			});
		}
	};
	
	$.fn.scroll = function(method){
		if(methods[method]){
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		}
		else{
			if(typeof(method) === "object" || typeof(method) === "undefined"){
				return methods.init.apply(this, arguments);
			}
			else{
				console.log("scroll: method \"" + method + "\" does not exist");
			}
		}
	};
	
})(jQuery);