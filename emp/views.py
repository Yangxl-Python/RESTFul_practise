from django.http import QueryDict
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, \
    CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from emp.models import Employees
from emp.serializers import EmployeesViewSerializer

from utils.response import EMPResponse


class EmployeesView(APIView):
    def get(self, request, *args, **kwargs):
        emp_id = kwargs.get('id')
        if emp_id:
            emp_obj = Employees.objects.filter(pk=emp_id, is_delete=False).first()
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
        return EMPResponse(data_status=200, data_message='success',
                           results=EmployeesViewSerializer(emp_obj, many=many).data)

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
        emp_id = kwargs.get('id')
        request_data = request.data
        emp_ids = list()

        if emp_id and isinstance(request_data, dict):
            emp_ids = [emp_id, ]
            request_data = [request_data, ]
        elif not emp_id and isinstance(request_data, list):
            for emp_dic in request_data:
                if emp_dic.get('id'):
                    emp_ids.append(emp_dic.pop('id'))
                else:
                    return Response({
                        'status': 500,
                        'message': 'id不存在'
                    })
        else:
            return Response({
                'status': 500,
                'message': '数据不存在或者格式有误'
            })

        new_data = list()
        emp_list = list()
        for index, emp_id in enumerate(emp_ids):
            try:
                emp_list.append(Employees.objects.get(pk=emp_id))
                new_data.append((request_data[index]))
            except:
                continue

        emp_ser = EmployeesViewSerializer(data=new_data, instance=emp_list, partial=True, many=True)
        emp_ser.is_valid(raise_exception=True)
        emp_ser.save()

        return Response({
            'status': 200,
            'message': 'success',
            'results': EmployeesViewSerializer(emp_list, many=True).data
        })


class EmployeesGenericAPIView(ListModelMixin,
                              RetrieveModelMixin,
                              CreateModelMixin,
                              UpdateModelMixin,
                              GenericAPIView):
    queryset = Employees.objects.filter(is_delete=False).all()
    serializer_class = EmployeesViewSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        # emp_list = self.get_queryset()
        # emp_ser = self.get_serializer(emp_list, many=True)
        # emp_data = emp_ser.data
        # return EMPResponse(200, 'success', emp_data)


        if 'id' in kwargs:
            response = self.retrieve(request, *args, **kwargs)
        else:
            response = self.list(request, *args, **kwargs)

        return EMPResponse(data_status=200, data_message='success',
                           results=response.data)

    def post(self, request, *args, **kwargs):
        return EMPResponse(200, 'success',
                           self.create(request, *args, **kwargs).data)

    def put(self, request, *args, **kwargs):
        return EMPResponse(200, 'success',
                           self.update(request, *args, **kwargs).data)

    def patch(self, request, *args, **kwargs):
        return EMPResponse(200, 'success',
                           self.partial_update(request, *args, **kwargs).data)


class EmployeeModelViewSet(ModelViewSet):
    queryset = Employees.objects.filter(is_delete=False)
    serializer_class = EmployeesViewSerializer
    lookup_field = 'id'

    def get_emp_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_emp_obj(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete_emp_obj(self, request, *args, **kwargs):
        emp_obj = self.get_object()
        if not emp_obj:
            return EMPResponse(500, '员工不存在或已删除')
        emp_obj.is_delete = True
        emp_obj.save()
        return EMPResponse(200, 'success')
