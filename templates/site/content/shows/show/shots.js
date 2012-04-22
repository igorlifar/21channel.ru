$("#shots-next").click(function() {
	$("#shots-slider").slider("moveleft", "109px");
});

$("#shots-prev").click(function() {
	$("#shots-slider").slider("moveright", "109px");
});

$("#shots-cont img").click(function(){
	var url_small = $(this).attr("src");
	var url_big = "";
	$("input[type=hidden]").each(function(){
		if($(this).attr("name") == url_small){
			url_big = $(this).val();
		}
	});
	for(var i = 0; i < shotsurls.length; i++){
		if(shotsurls[i] == url_big){
			$("#gallery-container").gallery("show", {"urls" : shotsurls, "shift" : i});
			break;
		}
	}
});