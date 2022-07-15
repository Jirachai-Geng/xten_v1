import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.common_util import ResponseMessage
from Apps.Authen.credentials import AuthenticateCredentials
from datetime import date, datetime, timedelta
import calendar


class ReportTOUService:
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
        select_month = request_data.get('select_month')
        range_time = self._get_start_end_month(select_month)
        start_time = range_time[0]
        end_time = range_time[1]

        try:
            print(select_month)
            end_time = (datetime.strptime(end_time, '%Y-%m-%d').date() + timedelta(1)).strftime('%Y-%m-%d')
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT trunc(extract(epoch from date(time) )*1000) as time_stm,
                        date(time) as time, max(kwh)-min(kwh) as data
                        FROM mdb where sensor_id = 1 and time between '{}' and '{}' 
                        group by date(time)
                        order by time_stm desc;""".format(start_time, end_time)
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            onPeak = self._onPeak(range_time)
            resStm = []
            resExport = []
            for object in selectObject:
                temp = []
                temp.append(object['time_stm'])
                temp.append(object['data'])
                temp_export = {
                    'time': object['time'],
                    'kWh': object['data'],
                    'offPeak': object['data']
                }
                resExport.append(temp_export)
                resStm.append(temp)

            resExport.pop(0)
            resStm.pop(0)

            for obj in resExport:
                for on_peak in onPeak['export']:
                    if obj['time'] == on_peak['time']:
                        obj['onPeak'] = on_peak['onPeak']
                        obj['offPeak'] = obj['kWh'] - obj['onPeak']


            graph_onpeak = []
            graph_offpeak = []

            for obj in resExport:
                temp_onpeak = []
                temp_offpeak = []
                temp_onpeak.append(obj['time'])
                temp_offpeak.append(obj['time'])
                if "onPeak" in obj:
                    temp_onpeak.append(obj['onPeak'])
                else:
                    temp_onpeak.append(0)
                temp_offpeak.append(obj['offPeak'])
                graph_offpeak.append(temp_offpeak)
                graph_onpeak.append(temp_onpeak)

            result = {
                'detail': {
                    'start_time': start_time,
                    'end_time': end_time
                }, 'data': {
                    'graph': resStm,
                    'graph_onpeak': graph_onpeak,
                    'graph_offpeak': graph_offpeak,
                    'export': resExport,
                }
            }
            response_return.set_success_status(result)

        except Exception as e:
            print(e)
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    def _onPeak(self, request_data):
        start_time = request_data[0]
        end_time = request_data[1]
        try:
            end_time = (datetime.strptime(end_time, '%Y-%m-%d').date() + timedelta(1)).strftime('%Y-%m-%d')
            conn = psycopg2.connect(self.connection)
            cursor = conn.cursor()
            query = """SELECT trunc(extract(epoch from date(time) )*1000) as time_stm, 
                        date(time) as time, max(kwh)-min(kwh) as data
                        FROM mdb where sensor_id = 1 and time between '{}' and '{}' 
                        and to_char(time, 'HH24:MI:SS') between '09:00:00' and '22:00:00' 
                        and EXTRACT(dow FROM time) NOT IN (0,6)
                        and date(time) NOT IN (
                        SELECT date(time) FROM public.holiday )
                        group by date(time)
                        order by time_stm desc;""".format(start_time, end_time)
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
                    'onPeak': object['data']
                }
                resExport.append(temp_export)
                resStm.append(temp)

            return {
                    'graph': resStm,
                    'export': resExport
                }

        except Exception as e:
            print(e)
            raise Exception("Exception Occurred _onPeak")

    def _get_start_end_month(self, input_):

        input_ = str(input_)

        year = int(input_[:4])
        month = int(input_[5:])

        start = """{}-{}-01""".format(year, input_[5:])
        end = """{}-{}-{}""".format(year, input_[5:], str(calendar.monthrange(year, month)[1]))

        return start, end
