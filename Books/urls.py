from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', views.user_login, name='login'),  
    path('register/', views.user_register, name='register'),  
]