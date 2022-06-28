from rest_framework.views import APIView
from rest_framework.response import Response

from BiullingService.invoice import InvoiceService
from XtenEngine.common_util import ResponseMessage


class Invoice(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        request_data = dict()
        request_data['billing_cycle'] = request.GET.get('billing_cycle', '')

        try:
            response_return = InvoiceService(request=request, token=request.META['HTTP_AUTHORIZATION']).getInvoice(request_data)
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)