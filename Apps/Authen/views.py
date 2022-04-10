from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from XtenEngine.common_util import ResponseMessage
from .authen import AuthenticateService


class Authenticate(APIView):
    @staticmethod
    def post(request):
        if not request.data:
            return Response({'Error': "Please provide email/password"}, status="400")
        response_return = ResponseMessage()
        request_data = dict()
        request_data['email'] = request.data.get('email', '')
        request_data['password'] = request.data.get('password', '')
        try:
            response_return = AuthenticateService(request=request).login(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)
