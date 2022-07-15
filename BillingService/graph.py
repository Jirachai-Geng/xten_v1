import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials
from datetime import date, datetime, timedelta


class GraphService:
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

    def data_graph(self, request_data):
        response_return = ResponseMessage()
        parameter = request_data.get('parameter')
        table = request_data.get('type')
        sensor_id = request_data.get('sensor_id')
        start_time = request_data.get('start_time')
        end_time = request_data.get('end_time')
        try:
            end_time = (datetime.strptime(end_time, '%Y-%m-%d').date() + timedelta(1)).strftime('%Y-%m-%d')
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT trunc(extract(epoch from time )*1000) as time_stm, 
                        to_char(time, 'DD/MM/YYYY HH24:MI:SS') as time,
                        {} as data FROM {} where sensor_id = {} and time between '{}' and '{}' 
                        order by time_stm desc;""".format(parameter, table, int(sensor_id), start_time, end_time)
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            resStm = []
            resExport = []
            for object in selectObject:
                temp = []
                temp.append(object['time_stm'])
                temp.append(object['data'])
                temp_export = {
                    'time': object['time'],
                    'kWh': object['data']
                }
                resExport.append(temp_export)
                resStm.append(temp)

            result = {
                'detail': {
                    'parameter': parameter,
                    'type': table,
                    'sensor_id': sensor_id,
                    'start_time': start_time,
                    'end_time': end_time
                }, 'data': {
                    'graph': resStm,
                    'export': resExport
                }
            }
            response_return.set_success_status(result)

        except Exception as e:
            print(e)
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()