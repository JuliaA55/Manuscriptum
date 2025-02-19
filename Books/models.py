from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, related_name='books')


    def __str__(self):
        return self.title
    
