from django.urls import path

from employee import views

urlpatterns = [
    path('employees/', views.EmployeeView.as_view()),
    path('employees/<str:id>/', views.EmployeeView.as_view()),
]
