from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Books
from book.serializers import BooksViewSerializer, BooksViewDeserializer, BooksViewSerializerV2


class BooksView(APIView):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        if book_id:
            book_obj = Books.objects.filter(pk=book_id, is_delete=False).first()
            if not book_obj:
                return Response({
                    'status': 500,
                    'message': '该图书不存在',
                })
            many = False
        else:
            book_obj = Books.objects.filter(is_delete=False)
            many = True
        return Response({
            'status': 200,
            'message': 'success',
            # 'result': BooksViewSerializer(book_obj, many=many).data,
            'result': BooksViewSerializerV2(book_obj, many=many).data,
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, QueryDict):
            request_data = request_data.dict()
        if isinstance(request_data, dict):
            # 添加单个
            many = False
        elif isinstance(request_data, list):
            # 添加多个
            many = True
        else:
            return Response({
                'status': 500,
                'message': '参数有误'
            })
        # ser_obj = BooksViewDeserializer(data=request_data, many=many)
        ser_obj = BooksViewSerializerV2(data=request_data, many=many)
        ser_obj.is_valid(raise_exception=True)
        book_obj = ser_obj.save()
        return Response({
            'status': 200,
            'message': 'success',
            # 'result': BooksViewSerializer(book_obj, many=many).data
            'result': BooksViewSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get('ids')
        book_obj = Books.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if book_obj:
            return Response({
                'status': 200,
                'message': 'success'
            })
        return Response({
            'status': 500,
            'message': '图书不存在或已删除'
        })

    def put(self, request, *args, partial=False, **kwargs):
        book_id = kwargs.get('id')
        request_data = request.data
        try:
            book_obj = Books.objects.get(pk=book_id, is_delete=False)
        except Exception as e:
            return Response({
                'status': 500,
                'message': e.args
            })
        serializer_obj = BooksViewSerializerV2(data=request_data, instance=book_obj, partial=partial)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        return Response({
            'status': 200,
            'message': 'success',
            'result': BooksViewSerializerV2(book_obj).data
        })

    def patch(self, request, *args, **kwargs):
        return self.put(request, args, partial=True, id=kwargs.get('id'))
