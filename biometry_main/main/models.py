from django.db import models

class user(models.Model):
    username = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=30, blank=False)
    voice = models.FileField()