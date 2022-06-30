import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials
from datetime import datetime
import calendar


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
            now = datetime.now()
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            if billing_cycle != "{}/{}".format(now.strftime("%Y"), now.strftime("%m")):
                query = """SELECT id, tenant, name_meter as meter_name, billing_cycle, energy_start,
                            energy_end as kwh, energy_use as energy_used, unit_price, revenue, leases_type
                            FROM public.billing_history WHERE billing_cycle LIKE '%{}%';""".format(billing_cycle)
            else:
                query = """SELECT sensors.name as meter_name, tenant.name as tenant, leases.leases_start, leases.leases_end,
                            leases.leases_type, energy_start.kwh as energy_start, energy.kwh, leases.unit_price
                            FROM public.leases
                            INNER JOIN public.sensors
                            ON leases.sensor_id = sensors.id
                            INNER JOIN public.tenant
                            ON leases.tenant_id = tenant.id
                            INNER JOIN (SELECT sensor_id, kwh
                                        FROM public.mdb
                                        WHERE time >= '{}'
                                        order by time asc
                                        LIMIT 1 ) energy_start
                           ON sensors.id = energy_start.sensor_id
                            INNER JOIN (SELECT sensor_id,kwh 
                                        FROM public.mdb
                                        ORDER BY time desc    
                                        LIMIT 1 ) energy
                            ON sensors.id = energy.sensor_id
                            """.format("{}-{}-01".format(now.strftime("%Y"), now.strftime("%m")))
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            for obj in selectObject:
                if billing_cycle == "{}/{}".format(now.strftime("%Y"), now.strftime("%m")):
                    obj['energy_used'] = obj['kwh'] - obj['energy_start']
                    obj['revenue'] = obj['energy_used'] * obj['unit_price']
                    if obj['leases_type'] == 1:
                        obj['leases_start'] = "{}/{}/01".format(now.strftime("%Y"), now.strftime("%m"))
                        obj['leases_end'] = "{}/{}/{}".format(now.strftime("%Y"), now.strftime("%m"),
                                            calendar.monthrange(int(now.strftime("%Y")), int(now.strftime("%m")))[1])
                        obj['billing_cycle'] = "{} - {}".format(obj['leases_start'], obj['leases_end'])


            response_return.set_success_status(selectObject)

        except Exception as e:
            print(e)
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()