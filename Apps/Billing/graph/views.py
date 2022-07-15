from rest_framework.views import APIView
from rest_framework.response import Response

from BillingService.graph import GraphService
from XtenEngine.common_util import ResponseMessage


class Graph(APIView):
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
            response_return = GraphService(request=request, token=request.META['HTTP_AUTHORIZATION']).data_graph(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)