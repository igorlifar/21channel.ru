from django.db import models

# Create your models here.

class Category(models.Model):

	title = models.CharField(max_length = 1000)
	priority = models.IntegerField()

class Page(models.Model):

	title = models.CharField(max_length = 1000)
	body = models.CharField(max_length = 10000)
	category = models.ForeignKey(Category, related_name = "pages")
	priority = models.IntegerField()