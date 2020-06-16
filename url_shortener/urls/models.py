from django.db import models
from django.contrib.auth.models import User


class Url(models.Model):
    origin_url = models.URLField(max_length=200)
    short_url = models.URLField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls_set')

    def __str__(self):
        return self.origin_url
