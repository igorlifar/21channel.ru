from django.db import models
from django.contrib.auth.models import User
from shows.models import Show
import datetime

class ShowComment(models.Model):
	
	show = models.ForeignKey(Show, related_name="comments")
	body = models.CharField(max_length=10000)
	date = models.DateTimeField(default = datetime.datetime.now)
	author = models.ForeignKey(User, related_name="show_commnets")
	


# Create your models here.
