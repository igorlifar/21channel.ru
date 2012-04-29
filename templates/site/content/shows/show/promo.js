$("#episode .cont").each(function() {
	console.log((document.documentElement.clientHeight - $(this).outerHeight()));
	console.log($(this).outerHeight());
	$(this).css('top', document.documentElement.clientHeight / 2 - $(this).outerHeight() / 2);
});

$("#episode .bg").click(function() {
	window.location.href=($("#episode-backlink").val());
});