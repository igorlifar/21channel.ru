$(document).ready(function() {
	$("#news li").each(function() {
		var nxt = $(this).find("div.view");
		var img = $(this).find("div.img");
		var info = $(this).find("div.info")
		$(this).mouseenter(function() {
			
			info.stop();
			nxt.stop();
			img.stop();
			
			info.animate({
				opacity: 0
			}, "fast", function() {
				$(this).css("display", "none");
			});
			
			img.animate({
				left: "450px"
			}, "medium");
			
			nxt.css("opacity", "0");
			nxt.css("display", "block");
			nxt.animate({
				opacity: 1
			}, "slow");
			
		})
		
		$(this).mouseleave(function() {
			info.stop();
			nxt.stop();
			img.stop();
			
			img.animate({
				left: "10px"
			}, "medium");
			
			info.css("opacity", "0");
			info.css("display", "block");
			info.animate({
				opacity: "1"
			}, "slow");
			
			nxt.animate({
				opacity: 0
			}, "fast", function() {
				$(this).css("display", "none");
			});
			
		})
	})
});