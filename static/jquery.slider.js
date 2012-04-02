(function($){
	
	var settings = {
		animationSpeed : "fast",
 		shift : 100
	};
	
	var methods = {
		init : function(overrideSettings){
			settings = $.extend(settings, overrideSettings);
		},
		moveleft : function(shift){
			if(typeof(shift) == "undefined"){
				shift = parseInt(settings.shift);
			}
			else{
				shift = parseInt(shift);
			}
			var container = this;
			if(container.data("state") == "locked"){
				return;
			}
			container.data("state", "locked");
			var content = container.children().eq(0);
			var containerWidth = container.outerWidth();
			var contentWidth = content.outerWidth();
			var currentShift = parseInt(content.css("left"));
			shift = Math.min(shift, currentShift + contentWidth - containerWidth);
			content.animate({
				"left" : "-=" + shift
			}, settings.animationSpeed, function(){
				container.data("state", "");
			});
		},
		moveright : function(shift){
			if(typeof(shift) == "undefined"){
				shift = parseInt(settings.shift);
			}
			else{
				shift = parseInt(shift);
			}
			var container = this;
			if(container.data("state") == "locked"){
				return;
			}
			container.data("state", "locked");
			var content = container.children().eq(0);
			var currentShift = parseInt(content.css("left"));
			shift = Math.min(shift, -currentShift);
			content.animate({
				"left" : "+=" + shift
			}, settings.animationSpeed, function(){
				container.data("state", "");
			});
		}
	};
	
	$.fn.slider = function(method){
		if(methods[method]){
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		}
		else{
			if(typeof(method) === "object" || typeof(method) === "undefined"){
				return methods.init.apply(this, arguments);
			}
			else{
				console.log("slider: method \"" + method + "\" does not exist");
			}
		}
	}
	
})(jQuery);