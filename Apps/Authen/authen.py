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
                        'rule': selectObject[0]['rule']
                    }
                    result = {
                        'token': jwt.encode(payload, SECRET_KEY, algorithm="HS256"),
                        'detail': {
                            'email': selectObject[0]['email'],
                            'username': selectObject[0]['username'],
                            'first_name': selectObject[0]['first_name'],
                            'last_name': selectObject[0]['last_name'],
                            'rule': selectObject[0]['rule']
                        }
                    }
                    response_return.set_success_status(result)
        except Exception as e:
            response_return.set_error_status('Exception Occurred')

        return response_return.get_response()

