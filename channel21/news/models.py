from django.db import models
import StringIO
from random import randint
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

class NewsItem(models.Model):
  
	title = models.CharField(max_length = 1000, blank = True)
	preview = models.CharField(max_length = 1000, blank = True)
	text = models.CharField(max_length = 10000, blank = True)
	date = models.DateTimeField(auto_now = True)
	image = models.ImageField(upload_to = "news/", blank = True)
  
	def load_image(self, img):
		content = ContentFile(img.read())
		content.seek(0)
		current = Image.open(content)
		current = ImageOps.fit(current, (300, 300), Image.ANTIALIAS)
		tmp = StringIO.StringIO()
		name = hex(randint(1, 10**50)) + ".jpg"
		current.save(tmp, "JPEG")
		tmp.seek(0)
		if self.image.__nonzero__():
			self.image.delete()
		self.image.save(name, ContentFile(tmp.read()))
		