from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', views.user_login, name='login'),  
    path('register/', views.user_register, name='register'),  
    path("logout/", views.user_logout, name="logout"),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path("books/<int:book_id>/read/", views.read_book, name="read_book"),
    path("books/<int:book_id>/download/", views.download_book, name="download_book"),
]