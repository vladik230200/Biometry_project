from django.db import models

class users(models.Model):
    username = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=64, blank=False)
    voice = models.BooleanField(default=False)

class samples(models.Model):
    id_user = models.ForeignKey(to=users, to_field='id', on_delete=models.CASCADE)
    sample = models.BinaryField(default=b"")
    features = models.JSONField()
