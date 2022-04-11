import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials


class ExploreService:
    def __init__(self, **kwargs):
        self.requests = requests
        self.token = kwargs.get('token', '')
        self.user_info = AuthenticateCredentials(self.token)
        self.connection = self.user_info['connection']

    def search_public_sensorTreeDiagram(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = "SELECT * FROM public.sensors;"
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            level_1 = []
            level_2 = []
            for i in range(len(selectObject)):
                if selectObject[i]['under_sensor'] is None:
                    level_1.append(selectObject[i])
                else:
                    level_2.append(selectObject[i])

            for i in range(len(level_1)):
                listUnderSensors = []
                for j in range(len(level_2)):
                    if level_1[i]['sensor_id'] == level_2[j]['under_sensor']:
                        listUnderSensors.append(level_2[j])
                level_1[i]['listUnderSensors'] = listUnderSensors

            response_return.set_success_status(level_1)

        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    def search_public_parameterMdb(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'mdb';"""
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            listParameter = []
            for data in selectObject:
                if data['column_name'] not in ('time','sensor_id'):
                    listParameter.append(data['column_name'])

            response_return.set_success_status(listParameter)

        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    def search_public_parameterMeter(self):
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'meter';"""
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            listParameter = []
            for data in selectObject:
                if data['column_name'] not in ('time', 'sensor_id'):
                    listParameter.append(data['column_name'])

            response_return.set_success_status(listParameter)

        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    def explore_data(self, request_data):
        response_return = ResponseMessage()
        parameter = request_data.get('parameter')
        table = request_data.get('type')
        sensor_id = request_data.get('sensor_id')
        start_time = request_data.get('start_time')
        end_time = request_data.get('end_time')
        try:
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            data = (int(sensor_id), start_time, end_time)
            query = """SELECT to_char(time, 'DD/MM/YYYY HH24:MI:SS') as time, {} as data FROM {} where sensor_id = %s and time between %s and %s order by time desc;""".format(parameter,table)
            cursor.execute(query, data)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]


            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            resTime = []
            resSeries = []
            for object in selectObject:
                if 'time' in object:
                    resTime.append(object['time'])
                if 'data' in object:
                    resSeries.append(object['data'])

            result = {
                'detail': {
                    'parameter': parameter,
                    'type': table,
                    'sensor_id': sensor_id,
                    'start_time': start_time,
                    'end_time': end_time
                },
                'data': {
                    'time': resTime,
                    'series': resSeries
                }
            }

            response_return.set_success_status(result)

        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()








