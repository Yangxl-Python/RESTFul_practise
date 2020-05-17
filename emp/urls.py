from django.urls import path

from emp import views

urlpatterns = [
    path('employees/', views.EmployeesView.as_view()),
    path('employees/<id>/', views.EmployeesView.as_view()),

    path('v1/employees/', views.EmployeesGenericAPIView.as_view()),
    path('v1/employees/<id>/', views.EmployeesGenericAPIView.as_view()),

    path('v2/employees/', views.EmployeeModelViewSet.as_view({'get': 'get_emp_list'})),
    path('v2/employees/<id>/', views.EmployeeModelViewSet.as_view({'get': 'get_emp_obj', 'delete': 'delete_emp_obj'})),
]