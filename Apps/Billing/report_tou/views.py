from rest_framework.views import APIView
from rest_framework.response import Response
from BillingService.report_tou import ReportTOUService
from XtenEngine.common_util import ResponseMessage


class Report_TOU(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        request_data = dict()
        request_data['select_month'] = request.GET.get('select_month', '')
        try:
            response_return = ReportTOUService(request=request, token=request.META['HTTP_AUTHORIZATION']).data_graph(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)