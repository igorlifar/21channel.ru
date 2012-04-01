from django.db import models
from shows.models import *
import StringIO
from random import randint
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.

class MainSettings(models.Model):
	
	show1 = models.ForeignKey(Show, related_name = "show1", blank = True, null = True)
	show2 = models.ForeignKey(Show, related_name = "show2", blank = True, null = True)
	show3 = models.ForeignKey(Show, related_name = "show3", blank = True, null = True)
	show4 = models.ForeignKey(Show, related_name = "show4", blank = True, null = True)
	show5 = models.ForeignKey(Show, related_name = "show5", blank = True, null = True)
	background = models.ImageField(upload_to = "settings/", blank = True)
	
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
		