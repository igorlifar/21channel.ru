from django.db import models
import StringIO
from random import randint
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

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
		name = hex(randint(1, 10**50)) + ".jpg"
		current.save(tmp, "JPEG")
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
		