from django.db import models
import StringIO
from random import randint
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import datetime

# Create your models here.

class Show(models.Model):
	
	title = models.CharField(max_length = 1000, blank = True)
	schedule = models.CharField(max_length = 1000, blank = True)
	description = models.CharField(max_length = 10000, blank = True)
	background = models.ImageField(upload_to = "shows/", blank = True)
	illustration = models.ImageField(upload_to = "shows/", blank = True)
	
	def load_image(self, img):
		content = ContentFile(img.read())
		content.seek(0)
		current = Image.open(content)
		tmp = StringIO.StringIO()
		name = hex(randint(1, 10**50)) + ".png"
		current.save(tmp, "PNG")
		tmp.seek(0)
		if self.background.__nonzero__():
			self.background.delete()
		self.background.save(name, ContentFile(tmp.read()))
		
	def load_illustration(self, img):
		content = ContentFile(img.read())
		content.seek(0)
		current = Image.open(content)
		current = ImageOps.fit(current, (497, 300), Image.ANTIALIAS)
		tmp = StringIO.StringIO()
		name = hex(randint(1, 10**50)) + ".jpg"
		current.save(tmp, "JPEG")
		tmp.seek(0)
		if self.illustration.__nonzero__():
			self.illustration.delete()
		self.illustration.save(name, ContentFile(tmp.read()))

class Shot(models.Model):
	
	shot_small = models.ImageField(upload_to = "shows/shots/", blank = True)
	shot_big = models.ImageField(upload_to = "shows/shots/", blank = True)
	show = models.ForeignKey(Show, related_name = "shows", blank = True, null = True)
	priority = models.IntegerField(blank = True, null = True)
	
	def load_shot(self, img):
		content = ContentFile(img.read())
		content.seek(0)
		current = Image.open(content)
		current = ImageOps.fit(current, (100, 70), Image.ANTIALIAS)
		tmp = StringIO.StringIO()
		name = hex(randint(1, 10**50)) + ".jpg"
		current.save(tmp, "JPEG")
		tmp.seek(0)
		if self.shot_small.__nonzero__():
			self.shot_small.delete()
		self.shot_small.save(name, ContentFile(tmp.read()))
		content.seek(0)
		current = Image.open(content)
		current = ImageOps.fit(current, (500, 350), Image.ANTIALIAS)
		tmp = StringIO.StringIO()
		name = hex(randint(1, 10**50)) + ".jpg"
		current.save(tmp, "JPEG")
		tmp.seek(0)
		if self.shot_big.__nonzero__():
			self.shot_big.delete()
		self.shot_big.save(name, ContentFile(tmp.read()))
		
		
class MetaItem(models.Model):
	
	key = models.CharField(max_length = 100, blank = True)
	value = models.CharField(max_length = 1000, blank = True)
	show = models.ForeignKey(Show, related_name = "mshows", blank = True, null = True)
	priority = models.IntegerField(blank = True, null = True)
	
	
class Article(models.Model):
	
	articletype_choices = (
		("A", "Article"),
		("R", "Review"),
	)
	
	articletype = models.CharField(max_length = 1, choices = articletype_choices, blank = True)
	title = models.CharField(max_length = 1000, blank = True)
	preview = models.CharField(max_length = 1000, blank = True)
	text = models.CharField(max_length = 10000, blank = True)
	author = models.CharField(max_length = 1000, blank = True)
	date = models.DateTimeField(default = datetime.datetime.now)
	show = models.ForeignKey(Show, related_name = "ashows", blank = True, null = True)
	priority = models.IntegerField(blank = True, null = True)