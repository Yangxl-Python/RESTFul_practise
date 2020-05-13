import traceback

from django.http import JsonResponse, QueryDict
from django.utils.decorators import method_decorator

from django.views import View
from django.views.decorators.csrf import csrf_exempt

from employee.models import Employee


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeView(View):
    def get(self, request, *args, **kwargs):
        emp_id = kwargs.get('id')
        if emp_id:
            emp = Employee.objects.filter(pk=emp_id).values('name', 'password', 'gender').first()
            if emp:
                return JsonResponse({
                    'status': 200,
                    'message': 'success',
                    'results': emp
                })
            else:
                return JsonResponse({
                    'status': 400,
                    'message': "This employee doesn't exist"
                })
        else:
            employees = Employee.objects.all().values('id', 'name', 'password', 'gender')
            return JsonResponse({
                'status': 200,
                'message': 'success',
                'results': list(employees)
            })

    def post(self, request, *args, **kwargs):
        try:
            rst = Employee.objects.create(**request.POST.dict())
            if rst:
                return JsonResponse({
                    'status': 200,
                    'message': 'success',
                    'results': {'name': rst.name,
                                'password': rst.password,
                                'gender': rst.gender}
                })
            else:
                return JsonResponse({
                    'status': 500,
                    'message': 'fail',
                })
        except Exception as e:
            traceback.print_exc()
            print(e)
            return JsonResponse({
                'status': 501,
                'message': '参数有误'
            })

    def put(self, request, *args, **kwargs):
        put = QueryDict(request.body)
        rst = Employee.objects.filter(pk=put.get('id'))
        try:
            if rst:
                rst = rst[0]
                rst.name = put.get('name')
                rst.password = put.get('password')
                rst.gender = put.get('gender')
                rst.save()
                return JsonResponse({
                    'status': 200,
                    'message': 'success'
                })
            else:
                return JsonResponse({
                    'status': 500,
                    'message': "This employee doesn't exist"
                })
        except Exception as e:
            traceback.print_exc()
            print(e)
            return JsonResponse({
                'status': 501,
                'message': '参数有误'
            })

    def delete(self, request, *args, **kwargs):
        delete = QueryDict(request.body)
        try:
            rst = Employee.objects.filter(pk=delete.get('id'))
            if rst:
                rst[0].delete()
                return JsonResponse({
                    'status': 200,
                    'message': 'success'
                })
            else:
                return JsonResponse({
                    'status': 500,
                    'message': "This employee doesn't exist"
                })
        except Exception as e:
            traceback.print_exc()
            print(e)
            return JsonResponse({
                'status': 501,
                'message': '参数有误'
            })

