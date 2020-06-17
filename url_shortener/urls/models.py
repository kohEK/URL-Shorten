from django.db import models
from django.contrib.auth.models import User


class Url(models.Model):
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls_set')
    origin_url = models.URLField(max_length=200)
    short_url = models.SlugField(max_length=6, primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.origin_url

# SlugField
