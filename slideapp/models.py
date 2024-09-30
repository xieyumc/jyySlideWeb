# slideapp/models.py

from django.db import models
from django.contrib.auth.models import User

class Slide(models.Model):
    title = models.CharField(max_length=200, default='未命名')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lock = models.BooleanField(default=True)
