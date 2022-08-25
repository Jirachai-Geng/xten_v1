import psycopg2
import requests
from django.http import JsonResponse
from XtenEngine.settings import CONNECTION, SECRET_KEY
from XtenEngine.common_util import ResponseMessage
import jwt
from cryptography.fernet import Fernet


class AuthenticateService:
    def __init__(self, **kwargs):
        self.requests = requests

    @staticmethod
    def login(request_data):
        response_return = ResponseMessage()
        email = request_data.get('email', '')
        username = request_data.get('username', '')
        password = request_data.get('password')
        try:
            conn = psycopg2.connect(CONNECTION)
            cursor = conn.cursor()
            query = f"SELECT * FROM public.auth_user where email = '{email}' or username = '{username}'"
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]
            for record in records:
                selectObject.append(dict(zip(columnNames, record)))
            if selectObject:
                fernet = Fernet(SECRET_KEY)
                print(type(selectObject[0]['password']))
                if password == fernet.decrypt(bytes(selectObject[0]['password'])).decode():
                    payload = {
                        'id': selectObject[0]['id'],
                        'email': selectObject[0]['email'],
                        'username': selectObject[0]['username'],
                        'project_id': selectObject[0]['project_id'],
                        'rule': selectObject[0]['rule'],
                        'logo_url': 'https://drive.google.com/uc?id={}&export=download'.format(selectObject[0]['logo_url'])
                    }
                    result = {
                        'token': jwt.encode(payload, SECRET_KEY, algorithm="HS256"),
                        'user_info': {
                            'email': selectObject[0]['email'],
                            'username': selectObject[0]['username'],
                            'first_name': selectObject[0]['first_name'],
                            'last_name': selectObject[0]['last_name'],
                            'rule': selectObject[0]['rule'],
                            'logo_url': 'https://drive.google.com/uc?id={}&export=download'.format(selectObject[0]['logo_url'])
                        }
                    }
                    response_return.set_success_status(result)
        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    @staticmethod
    def register(request_data):
        response_return = ResponseMessage()
        email = request_data.get('email', '')
        password = request_data.get('password')
        first_name = request_data.get('first_name', '')
        last_name = request_data.get('last_name', '')

        try:
            conn = psycopg2.connect(CONNECTION)
            cursor = conn.cursor()
            query = f"SELECT * FROM public.auth_user where email = '{email}'"
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]
            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            if selectObject:
                if selectObject[0]['change_pass']:
                    fernet = Fernet(SECRET_KEY)
                    encPassword = fernet.encrypt(password.encode())
                    print(type(selectObject[0]['password']))
                    SQL = f"UPDATE public.auth_user SET password = '{encPassword.decode('ascii')}' " \
                          f", first_name='{first_name}', last_name='{last_name}', change_pass=false " \
                          f"WHERE email = '{email}'"
                    cursor.execute(SQL)
                    conn.commit()
                    cursor.close()

                response_return.set_success_status()
        except Exception as e:
            response_return.set_error_status('Exception Occurred')
        return response_return.get_response()

    @staticmethod
    def canRegister(request_data):
        response_return = ResponseMessage()
        userid = request_data.get('userid', '')
        try:
            conn = psycopg2.connect(CONNECTION)
            cursor = conn.cursor()
            query = f"SELECT * FROM public.auth_user where uuid = '{userid}'"
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))

            result = {
                'email': selectObject[0]['email']
            }

            response_return.set_success_status(result)
        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    @staticmethod
    def test(request_data):
        response_return = ResponseMessage()
        type = request_data.get('type', '')
        name = request_data.get('name', '')
        score = request_data.get('score', '')

        try:
            conn = psycopg2.connect(CONNECTION)
            cursor = conn.cursor()
            SQL = f"INSERT INTO test(type, name, score)VALUES ('{type}', '{name}', {score}) 	" \
                    f"ON CONFLICT(name) DO UPDATE " \
                    f"SET type = EXCLUDED.type, score = EXCLUDED.score"
            cursor.execute(SQL)
            conn.commit()
            cursor.close()

            response_return.set_success_status()
        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

    @staticmethod
    def testShare(request_data):
        response_return = ResponseMessage()
        score = request_data.get('score', '')
        try:
            html = """<!DOCTYPE html>
                        <html lang="en">
                         <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <meta property="og:title" content="European Travel Destinations">
                                <meta property="og:type" content="article" />
                                <meta property="og:description" content="Offering tour packages for individuals or groups. score = {}">
                                <meta property="og:image" content="http://euro-travel-example.com/thumbnail.jpg">
                                <meta property="og:url" content="http://euro-travel-example.com/index.htm">
                            
                                <title>AppName</title>
                            </head>
                         <body>
                         </body>
                        </html>""".format(score)

            response_return.set_success_status(html)
        except Exception as e:
            response_return.set_error_status('Exception Occurred')
        return response_return.get_response()


    @staticmethod
    def testGetScore():
        response_return = ResponseMessage()
        try:
            conn = psycopg2.connect(CONNECTION)
            cursor = conn.cursor()
            query = """SELECT type, score, name FROM public.test order by score desc;"""
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]

            for record in records:
                selectObject.append(dict(zip(columnNames, record)))
            index = 0
            result = []
            for object in selectObject:
                index = index + 1
                temp = {
                    'id': index,
                    'fullName': object['name'],
                    'score': object['score'],
                }
                result.append(temp)

            response_return.set_success_status(result)
        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

