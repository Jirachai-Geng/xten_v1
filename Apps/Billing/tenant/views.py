from rest_framework.views import APIView
from rest_framework.response import Response

from BiullingService.tenant import TenantService
from XtenEngine.common_util import ResponseMessage


class Tenant(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = TenantService(request=request, token=request.META['HTTP_AUTHORIZATION']).getTenant()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)