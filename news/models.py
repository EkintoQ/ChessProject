from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    date = models.TextField()
    body = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
