import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials


class InvoiceService:
    def __init__(self, **kwargs):
        self.requests = requests
        self.token = kwargs.get('token', '')
        self.user_info = AuthenticateCredentials(self.token)
        self.connection = self.user_info['connection']

    def getInvoice(self, request_data):
        response_return = ResponseMessage()
        billing_cycle = request_data.get('billing_cycle')
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT sensors.name as meter_name, tenant.name as tenant, 
                        leases.leases_type, billing_history.energy_end as last_bill, energy.kwh, leases.unit_price
                        FROM public.leases
                        INNER JOIN public.sensors
                        ON leases.sensor_id = sensors.id
                        INNER JOIN public.tenant
                        ON leases.tenant_id = tenant.id
                        INNER JOIN (SELECT tenant, energy_end
                                    FROM public.billing_history
                                    order by billing_cycle desc
                                    limit 1 ) billing_history
                        ON tenant.name = billing_history.tenant
                        INNER JOIN (SELECT sensor_id,kwh 
                                    FROM public.mdb
                                    ORDER BY time desc    
                                    LIMIT 1 ) energy
                        ON sensors.id = energy.sensor_id
                        """
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            for obj in selectObject:
                obj['energy_used'] = obj['kwh'] - obj['last_bill']
                obj['revenue'] = obj['energy_used'] * obj['unit_price']

            response_return.set_success_status(selectObject)

        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()