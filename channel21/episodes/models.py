from django.db import models
from shows.models import *

# Create your models here.

class Video(models.Model):
	
	source_choices = (
		("Y", "YouTube"),
	)
	
	source = models.CharField(max_length = 1, choices = source_choices, blank = True)
	code = models.CharField(max_length = 100, blank = True)
	
	def get_screen_shot(self):
		if self.source == "Y":
			return "http://img.youtube.com/vi/" + self.code + "/0.jpg"
		return "undefined"
		
	def get_player(self, width, height):
		if self.source == "Y":
			return '<object height="' + str(height) + '" width="' + str(width) + '"><param name="movie" value="http://www.youtube.com/v/' + self.code + '"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/' + self.code + '" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="' + str(width) + '" height="' + str(height) + '"></embed></object>'
		return "undefined"
		
class Episode(models.Model):
	
	episodetype_choices = (
		("I", "Issue"),
		("E", "Episode"),
		("P", "Promo"),
	)
	
	video = models.ForeignKey(Video, related_name = 'video', blank = True, null = True)
	show = models.ForeignKey(Show, related_name = 'show', blank = True, null = True)
	date = models.DateTimeField(auto_now = True)
	episodetype = models.CharField(max_length = 1, choices = episodetype_choices, blank = True, default = "E")
	title = models.CharField(max_length = 1000, blank = True)
	description = models.CharField(max_length = 10000, blank = True)
	