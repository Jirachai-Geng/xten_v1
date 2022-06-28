from rest_framework.views import APIView
from rest_framework.response import Response

from BiullingService.leases import LeasesService
from XtenEngine.common_util import ResponseMessage


class Leases(APIView):
    @staticmethod
    def get(request):
        response_return = ResponseMessage()
        try:
            response_return = LeasesService(request=request, token=request.META['HTTP_AUTHORIZATION']).getLeases()
            return Response(response_return)
        except Exception:
            response_return.set_error_status('Exception Occurred')
            return Response(response_return)