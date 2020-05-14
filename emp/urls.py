from django.urls import path

from emp import views

urlpatterns = [
    path('employees/', views.EmployeesView.as_view()),
    path('employees/<id>/', views.EmployeesView.as_view()),
]