from django.shortcuts import render
from .models import Book

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        books = books.filter(title__istartswith=search_query) | books.filter(title__icontains=search_query)

    return render(request, 'books/book_list.html', {'books': books})