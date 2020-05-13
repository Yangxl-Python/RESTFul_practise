import traceback

# Create your views here.
from django.http import QueryDict
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from student.models import Student

from .serializers import StudentModelSerializer, StudentModelDeserializer


class StudentView(APIView):
    # renderer_classes = [BrowsableAPIRenderer]
    # parser_classes = [JSONParser]
    # parser_classes = [FormParser]
    # parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        stu_id = kwargs.get('id')
        if stu_id:
            rst = Student.objects.filter(pk=stu_id).first()
            if rst:
                return Response({
                    'status': 200,
                    'message': 'success',
                    'results': StudentModelSerializer(rst).data
                })
            else:
                return Response({
                    'status': 500,
                    'message': "This student doesn't exist",
                })
        else:
            rst = Student.objects.all()
            return Response({
                'status': 200,
                'message': "success",
                'results': StudentModelSerializer(rst, many=True).data
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, QueryDict):
            request_data = request_data.dict()
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                'status': 501,
                'message': '参数有误'
            })
        try:
            deserializer = StudentModelDeserializer(data=request_data)
            if deserializer.is_valid():
                return Response({
                    'status': 200,
                    'message': 'success',
                    'results': StudentModelSerializer(deserializer.save()).data
                })
            else:
                return Response({
                    'status': 500,
                    'message': deserializer.errors,
                })
        except Exception as e:
            traceback.print_exc()
            print(e)
            return Response({
                'status': 502,
                'message': '服务器内部错误'
            })

