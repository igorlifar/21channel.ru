function getScreen(url){
  var vid;
  var results;
  results = url.match("[\\?&]v=([^&#]*)");
  vid = (results === null) ? url : results[1];
  return "http://img.youtube.com/vi/" + vid + "/0.jpg";
}

var fillSettings = {
	rightDist : "5px",
	bottomDist : "5px",
	imgButton : "/static_files/img/watch.png"
};

function fillContainer(container, code, width, height){
	container.html('<img src="' + getScreen(code) + '" width="' + width + '" height="' + height + '"><img src="' + fillSettings.imgButton + '"></img>');
	container.css("position", "relative");
	container.css("width", width);
	current = container.children().eq(1);
	current.css("position", "absolute");
	current.css("right", fillSettings.rightDist);
	current.css("bottom", fillSettings.bottomDist);
	current.css("cursor", "pointer");
	current.data("height", height);
	current.data("width", width);
	current.data("code", code);
	current.click(function(){
		var container = $(this).parent();
		var height = $(this).data("height");
		var width = $(this).data("width");
		var code = $(this).data("code");
		container.html('<object height="' + height + '" width="' + width + '"><param name="movie" value="http://www.youtube.com/v/' + code + '"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/' + code + '" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="' + width + '" height="' + height + '"></embed></object>');
	});
}