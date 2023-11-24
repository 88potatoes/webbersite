from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    authors = models.CharField(max_length=255)
    date = models.DateField()
    # invisible articles should still be viewable, just they do not show up on the listed articles page
    visible = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title
