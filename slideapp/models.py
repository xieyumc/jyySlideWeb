from django.db import models
from django.contrib.auth.models import User

class Slide(models.Model):
    title = models.CharField(max_length=200, default='未命名')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lock = models.BooleanField(default=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slides')

    def __str__(self):
        return self.title

class SlideVersion(models.Model):
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE, related_name='versions')
    content = models.TextField()
    saved_at = models.DateTimeField(auto_now_add=True)
    saved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-saved_at']

    def __str__(self):
        return f"Version saved at {self.saved_at} by {self.saved_by}"
