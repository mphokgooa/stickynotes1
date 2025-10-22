from django.db import models
from django.conf import settings

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
