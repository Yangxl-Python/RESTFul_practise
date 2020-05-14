from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView

from emp.models import Employees
from emp.serializers import EmployeesViewSerializer


class EmployeesView(APIView):
    def get(self, request, *args, **kwargs):
        emp_id = kwargs.get('id')
        if emp_id:
            emp_obj = Employees.objects.filter(pk=emp_id, is_delete=False)
            if emp_obj:
                many = False
            else:
                return Response({
                    'status': 500,
                    'message': '该员工不存在',
                })
        else:
            emp_obj = Employees.objects.filter(is_delete=False)
            many = True
        return Response({
            'status': 200,
            'message': 'success',
            'result': EmployeesViewSerializer(emp_obj, many=many).data
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, QueryDict):
            request_data = request_data.dict()
        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                'status': 500,
                'message': '参数有误',
            })
        emp_ser = EmployeesViewSerializer(data=request_data, many=many)
        emp_ser.is_valid(raise_exception=True)
        emp_obj = emp_ser.save()
        return Response({
            'status': 200,
            'message': 'success',
            'result': EmployeesViewSerializer(emp_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        emp_id = kwargs.get('id')
        if emp_id:
            ids = [emp_id]
        else:
            ids = request.data.get('ids')
        emp_objs = Employees.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if emp_objs:
            return Response({
                'status': 200,
                'message': 'success'
            })
        return Response({
            'status': 500,
            'message': '员工不存在或已删除'
        })

    def put(self, request, *args, partial=False, **kwargs):
        emp_id = kwargs.get('id')
        request_data = request.data
        try:
            emp_obj = Employees.objects.get(pk=emp_id, is_delete=False)
        except Exception as e:
            return Response({
                'status': 500,
                'message': e.args
            })
        emp_ser = EmployeesViewSerializer(data=request_data, instance=emp_obj, partial=partial)
        emp_ser.is_valid(raise_exception=True)
        emp_ser.save()
        return Response({
            'status': 200,
            'message': 'success',
            'result': EmployeesViewSerializer(emp_obj).data
        })

    def patch(self, request, *args, **kwargs):
        return self.put(request, args, partial=True, id=kwargs.get('id'))
