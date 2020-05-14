from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as eh


def exception_handler(exc, context):
    response = eh(exc, context)
    if response is None:
        return Response({
            'error': '程序走神了，请稍等一会~',
            'message': str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
