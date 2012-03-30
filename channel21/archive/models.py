from django.db import models
from episodes.models import *

# Create your models here.

class Archive(models.Model):
	
	title = models.CharField(max_length = 1000, blank = True)
	episodes = models.ManyToManyField(Episode, blank = True)