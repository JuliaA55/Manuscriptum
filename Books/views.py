from django.shortcuts import render, redirect
from .models import Book
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        books = books.filter(title__istartswith=search_query) | books.filter(title__icontains=search_query)

    return render(request, 'books/book_list.html', {'books': books})



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