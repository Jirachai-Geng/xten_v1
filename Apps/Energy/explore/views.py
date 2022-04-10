from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from XtenEngine.common_util import ResponseMessage
from EnergyService.explore import ExploreService


class ExploreData(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        request_data = dict()
        request_data['parameter'] = request.GET.get('parameter', '')
        request_data['type'] = request.GET.get('type', '')
        request_data['sensor_id'] = request.GET.get('sensor_id', '')
        request_data['start_time'] = request.GET.get('start_time', '')
        request_data['end_time'] = request.GET.get('end_time', '')
        try:
            response_return = ExploreService(request=request, token=request.META['HTTP_AUTHORIZATION']).explore_data(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class SearchPublicSensorTreeDiagram(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = ExploreService(request=request, token=request.META['HTTP_AUTHORIZATION']).search_public_sensorTreeDiagram()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class SearchPublicParameterMdb(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = ExploreService(request=request, token=request.META['HTTP_AUTHORIZATION']).search_public_parameterMdb()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)


class SearchPublicParameterMeter(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = ExploreService(request=request, token=request.META['HTTP_AUTHORIZATION']).search_public_parameterMeter()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)

