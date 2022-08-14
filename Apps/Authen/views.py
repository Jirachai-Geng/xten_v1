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
        request_data['username'] = request.data.get('username', '')
        try:
            response_return = AuthenticateService(request=request).login(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class Register(APIView):
    @staticmethod
    def get(request):
        if not request.data:
            return Response({'Error': "Please provide email/password"}, status="400")
        response_return = ResponseMessage()
        request_data = dict()
        request_data['email'] = request.data.get('email', '')
        request_data['password'] = request.data.get('password', '')
        request_data['username'] = request.data.get('username', '')
        try:
            response_return = AuthenticateService(request=request).register(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class GameShare(APIView):
    @staticmethod
    def get(request):
        if not request.data:
            return Response({'Error': "something wrong"}, status="400")
        response_return = ResponseMessage()
        request_data = dict()
        request_data['score'] = request.data.get('score', '')
        try:
            response_return = AuthenticateService(request=request).testShare(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class GameScore(APIView):
    @staticmethod
    def post(request):
        if not request.data:
            return Response({'Error': "something wrong"}, status="400")
        response_return = ResponseMessage()
        request_data = dict()
        request_data['type'] = request.data.get('type', '')
        request_data['name'] = request.data.get('name', '')
        request_data['score'] = request.data.get('score', '')
        try:
            response_return = AuthenticateService(request=request).test(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class CanRegister(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        request_data = dict()
        request_data['userid'] = request.GET.get('userid', '')
        try:
            response_return = AuthenticateService(request=request).canRegister(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)