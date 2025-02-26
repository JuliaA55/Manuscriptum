from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category,Author
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import os
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    search_query = request.GET.get('search')
    category_id = request.GET.get('category_id')
    categories = Category.objects.all()

    if search_query:
        books = books.filter(title__istartswith=search_query) | books.filter(title__icontains=search_query)
    if category_id:
        books = Book.objects.filter(category_id=category_id)

    return render(request, 'books/book_list.html', {'books': books, "categories":categories})

def book_detail(request,id):
    book = get_object_or_404(Book, id=id)

    return render(request, 'books/book_detail.html', {'book': book})

TEXT_FILES_DIR = "media/files/" 

def read_book(request, book_id):
    """ Відображає сторінку для читання книги """
    book = get_object_or_404(Book, id=book_id)
    file_path = book.text.path

    if not os.path.exists(file_path):
        return render(request, "404.html", status=404)

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().split("\n") 

    paginator = Paginator(text, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "books/read_book.html", {
        "book": book,
        "page_obj": page_obj
    })

def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.text:
        raise Http404("Файл книги не знайдено.")
    return FileResponse(book.text.open('rb'), as_attachment=True, filename=book.text.name.split('/')[-1])

def user_login(request):
    """Обробка входу користувача"""
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect("book_list")  
    return render(request, "books/auth.html", {"form": form, "page": "login"})

def user_register(request):
    """Обробка реєстрації нового користувача"""
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )
        login(request, user)  
        return redirect("book_list")
    return render(request, "books/auth.html", {"form": form, "page": "register"})


def user_logout(request):
    """Обробка виходу користувача"""
    logout(request)
    return redirect("book_list") 


@login_required
def favorite_books(request):
    liked_books = request.user.liked_books.all()
    return render(request, 'books/favorite_books.html', {'books': liked_books})


@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.user in book.likes.all():
        book.likes.remove(request.user)
    else:
        book.likes.add(request.user)


    return redirect("book_list")

def category_book(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})

def authors(request):
    authors_data = [
        {
            'name': 'Денис',
            'role': 'Developer',
            'description': 'Опис автора 1',
            'image': '/media/images/dev.png'
        },
        {
            'name': 'Юлія',
            'role': 'Developer/TeamLead ',
            'description': 'Опис автора 2',
            'image': '/media/images/dev.png'
        },
        {
            'name': 'Ілля',
            'role': 'Developer',
            'description': 'Опис автора 3',
            'image': '/media/images/dev.png'
        },
        {
            'name': 'Владислав',
            'role': 'Developer',
            'description': 'Опис автора 4',
            'image': '/media/images/dev.png'
        }
    ]
    return render(request, 'books/authors.html', {'authors': authors_data})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.books.all()
    return render(request, 'books/author_detail.html', {'author': author, 'books': books})