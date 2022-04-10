import token

import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials


class PowerQualityService:
    def __init__(self, **kwargs):
        self.requests = requests
        self.token = kwargs.get('token', '')
        self.user_info = AuthenticateCredentials(self.token)
        self.connection = self.user_info['connection']

    def getDataMdb(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = "SELECT tt.* FROM public.mdb tt INNER JOIN (SELECT sensor_id, MAX(time) AS MaxDateTime " \
                    "FROM public.mdb GROUP BY sensor_id) groupedtt ON tt.sensor_id = groupedtt.sensor_id " \
                    "AND tt.time = groupedtt.MaxDateTime"
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

    def getDataSensor(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = "SELECT tt.* FROM public.meter tt INNER JOIN (SELECT sensor_id, MAX(time) AS MaxDateTime " \
                    "FROM public.meter GROUP BY sensor_id) groupedtt ON tt.sensor_id = groupedtt.sensor_id " \
                    "AND tt.time = groupedtt.MaxDateTime"
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

    def search_public_sensorMdb(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT sensor_id, name, type, location
                    FROM public.sensors
                    where type = 'mdb'"""
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



