import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials


class LeasesService:
    def __init__(self, **kwargs):
        self.requests = requests
        self.token = kwargs.get('token', '')
        self.user_info = AuthenticateCredentials(self.token)
        self.connection = self.user_info['connection']

    def getLeases(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT leases.sensor_id, tenant.name as tenant_name , leases.leases_type, 
                        sensors.name as meter_name, sensors.location, sensors.zone, sensors.model, sensors.serial,
                        sensors.install_date, leases.unit_price
                        FROM public.leases
                        INNER JOIN public.sensors
                        ON leases.sensor_id = sensors.id
                        INNER JOIN public.tenant
                        ON leases.tenant_id = tenant.id"""
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            response_return.set_success_status(selectObject)

        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()