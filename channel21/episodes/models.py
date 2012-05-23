from django.db import models
from shows.models import *
import datetime
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

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
	date = models.DateTimeField(default = datetime.datetime.now)
	episodetype = models.CharField(max_length = 1, choices = episodetype_choices, blank = True, default = "E")
	title = models.CharField(max_length = 1000, blank = True)
	description = models.CharField(max_length = 10000, blank = True)

	def clear_cache(self):
		templates = ['screenshot', 'video', 'link']
		keys = ['episode-'+ str(self.id) + '-' + x for x in templates]
		cache.delete_many(keys)

	def get_screenshot(self):

		key = 'episode-' + str(self.id) + '-screenshot'
		s = cache.get(key)

		if s is None:
			print 'not cached'
			s = self.video.get_screen_shot()
			cache.set(key, s, 60*60*5)

		return s

	def get_video(self):
		key = 'episode-' + str(self.id) + '-video'
		video = cache.get(key)

		print key, video

		if video is None:
			video = self.video
			cache.set(key, video, 60*60*5)

		return video

	def get_link(self):
		key = 'episode-'+ str(self.id) + '-link'
		link = cache.get(key)

		if link is None:
			if not self.show == None:
				if self.episodetype == 'I':
					link = "/shows/" + str(self.show.id) + "/issues/watch/" + str(self.id) + "/"
				elif self.episodetype == 'E':
					link = "/shows/" + str(self.show.id) + "/episodes/watch/" + str(self.id) + "/"
				else:
					link = "/shows/" + str(self.show.id) + "/promo/watch/" + str(self.id) + "/"
			else:
				link = "/episode/" + str(self.id) + "/"

			cache.set(key, link, 60*60*5)

		return link

@receiver(post_save, sender=Video)
def video_cache_post_save(sender, **kwargs):
    video = kwargs['instance']
    for episode in video.video.all():
    	episode.clear_cache()

    
@receiver(post_save, sender=Episode)
def episode_cache_post_save(sender, **kwargs):
    episode = kwargs['instance']
    episode.clear_cache()





	