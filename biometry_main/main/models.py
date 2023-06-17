from django.db import models

class users(models.Model):
    username = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=64, blank=False)
    voice = models.BooleanField(default=False)

class samples(models.Model):
    username = models.CharField(max_length=30, blank=False)
    models.BinaryField()