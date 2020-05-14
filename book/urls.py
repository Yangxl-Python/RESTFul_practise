from django.urls import path

from book import views

urlpatterns = [
    path('books/', views.BooksView.as_view()),
    path('books/<id>/', views.BooksView.as_view()),
]
