from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from XtenEngine.common_util import ResponseMessage
from .authen import AuthenticateService
from django.http import HttpResponse
from django.template import Context, loader
from rest_framework.renderers import TemplateHTMLRenderer


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


class AuthenticateTEST(APIView):
    @staticmethod
    def post(request):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")
        response_return = ResponseMessage()
        request_data = dict()
        request_data['password'] = request.data.get('password', '')
        request_data['username'] = request.data.get('username', '')
        try:
            response_return = AuthenticateService(request=request).loginTEST(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class Register(APIView):
    @staticmethod
    def post(request):
        if not request.data:
            return Response({'Error': "Please provide email/password"}, status="400")
        response_return = ResponseMessage()
        request_data = dict()
        request_data['email'] = request.data.get('email', '')
        request_data['password'] = request.data.get('password', '')
        request_data['first_name'] = request.data.get('first_name', '')
        request_data['last_name'] = request.data.get('last_name', '')
        try:
            response_return = AuthenticateService(request=request).register(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class GameShare(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        request_data = dict()
        request_data['score'] = request.GET.get('score', '')
        try:
            # response_return = AuthenticateService(request=request).testShare(request_data)
            html = """<html lang="en">
                                     <head>
                                            <meta charset="UTF-8">
                                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                            <meta property="og:title" content=" title text score = {}">
                                            <meta property="og:type" content="article" />
                                            <meta property="og:description" content="description text">
                                            <meta property="og:image" content="https://picsum.photos/200">

                                            <title>AppName</title>
                                        </head>
                                     <body>
                                     </body>
                                    </html>""".format(request_data['score'])
            return HttpResponse(html)
            # return Response(html)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class GameScore(APIView):
    @staticmethod
    def post(request):
        if not request.data:
            return Response({'Error': "something wrong"}, status="400")
        response_return = ResponseMessage()
        request_data = request.data.get("data")
        try:
            response_return = AuthenticateService(request=request).test(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class GameGetScore(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = AuthenticateService(request=request).testGetScore()
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