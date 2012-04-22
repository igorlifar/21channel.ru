$(".preview a").click(function() {
	var show = $(this).parent().parent().parent().find(".full");
	var hide = $(this).parent().parent();
	
	console.log(show);
	console.log(hide);
	
	$(".full").css("display", "none");
	$(".preview").css("display", "block");
	setTimeout(function() {
		hide.css("display", "none");
		show.css("display", "block");
	}, 10);
});
		