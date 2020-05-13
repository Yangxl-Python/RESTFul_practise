from django.urls import path

from student import views

urlpatterns = [
    path('students/', views.StudentView.as_view()),
    path('students/<str:id>/', views.StudentView.as_view()),
]