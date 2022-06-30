import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials
import datetime
from django.utils import timezone


class TenantService:
    def __init__(self, **kwargs):
        self.requests = requests
        self.token = kwargs.get('token', '')
        self.user_info = AuthenticateCredentials(self.token)
        self.connection = self.user_info['connection']

    def getTenant(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT tenant.id, tenant.name, email, create_date, count(leases.tenant_id) as number_of_tenant,
                        SUM (billing_history.revenue) AS total_revenue, leases.leases_start, leases.leases_end, 
                        billing_last.energy_end as last_bill, energy_end.kwh, leases.unit_price
                        FROM public.tenant
                        INNER JOIN public.leases
                        ON tenant.id = leases.tenant_id
                        INNER JOIN public.billing_history
                        ON tenant.name = billing_history.tenant
                        INNER JOIN (SELECT tenant, energy_end
                                FROM public.billing_history
                                order by billing_cycle desc
                                limit 1 ) billing_last
                        ON tenant.name = billing_history.tenant
                        INNER JOIN (SELECT sensor_id,kwh 
                                FROM public.mdb
                                ORDER BY time desc    
                                LIMIT 1 ) energy_end
                        ON leases.sensor_id = energy_end.sensor_id
                        group by tenant.id,leases.id,energy_end.kwh,billing_last.energy_end"""
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            for obj in selectObject:
                obj['status'] = self._checkStatusLeases(obj['leases_start'], obj['leases_end'])
                obj['revenue_incoming'] = (obj['kwh'] - obj['last_bill'])* obj['unit_price']

            response_return.set_success_status(selectObject)

        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    @staticmethod
    def _checkStatusLeases(leases_start, leases_end):
        today = timezone.now()
        try:
            if leases_start <= today <= leases_end:
                return 'on renting'
            else:
                return 'out of contract'
        except Exception as e:
            return 'Exception {}'.format(e)

