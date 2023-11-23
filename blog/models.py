from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    authors = models.CharField(max_length=255)
    date = models.DateField()
    

    def __str__(self):
        return self.title
