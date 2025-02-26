from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}"

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(max_length=500)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

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
    authorId = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='books')


    def __str__(self):
        return self.title
    
