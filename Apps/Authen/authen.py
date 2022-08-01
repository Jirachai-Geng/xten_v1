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
                if selectObject[0]['password'] == 'false':
                    fernet = Fernet(SECRET_KEY)
                    encPassword = fernet.encrypt(password.encode())
                    print(type(selectObject[0]['password']))
                    SQL = f"UPDATE public.auth_user SET password = '{encPassword.decode('ascii')}' " \
                          f", first_name={first_name}, last_name={last_name} WHERE email = '{email}'"
                    cursor.execute(SQL)
                    conn.commit()
                    cursor.close()

                response_return.set_success_status()
        except Exception as e:
            response_return.set_error_status('Exception Occurred')

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

