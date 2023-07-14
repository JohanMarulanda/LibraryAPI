from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    authors = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    publication_date = models.DateField()
    editor = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(blank=True)

    def _str_(self):
        return self.title