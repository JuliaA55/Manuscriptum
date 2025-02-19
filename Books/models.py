from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    numberOfPages = models.IntegerField()
    genre = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    text = models.FileField(upload_to='files/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="liked_books", blank=True)

    def __str__(self):
        return self.title
    
    def get_content(self):
        if self.text:
            with self.text.open('r', encoding='utf-8') as f:
                return f.read()
        return "No content available"
