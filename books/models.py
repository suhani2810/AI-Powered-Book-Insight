from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    rating = models.CharField(max_length=20)
    link = models.URLField()
    description = models.TextField()
    summary = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=100, default="Unknown")
    recommendation = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.title