from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from XtenEngine.common_util import ResponseMessage
from EnergyService.power_quality import PowerQualityService


class PowerQuality(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = PowerQualityService(request=request, token=request.META['HTTP_AUTHORIZATION']).getDataMdb()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class AllMeter(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = PowerQualityService(request=request, token=request.META['HTTP_AUTHORIZATION']).getDataAllMeter()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class SearchPublicSensorMdb(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = PowerQualityService(request=request, token=request.META['HTTP_AUTHORIZATION']).search_public_sensorMdb()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)
