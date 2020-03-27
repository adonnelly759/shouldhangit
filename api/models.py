from django.db import models

class Key(models.Model):
    site = models.CharField(max_length=255)
    key = models.CharField(max_length=255)

class Search(models.Model):
    location = models.CharField(max_length=255)
    ip = models.CharField(max_length=255, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.location).capitalize()