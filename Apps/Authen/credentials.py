import psycopg2
from XtenEngine.settings import CONNECTION, SECRET_KEY
from XtenEngine.common_util import ResponseMessage
import jwt


def AuthenticateCredentials(request_data):
    response_return = ResponseMessage()
    decoded = jwt.decode(request_data[len('Bearer '):], SECRET_KEY, algorithms="HS256")
    try:
        if decoded:
            conn = psycopg2.connect(CONNECTION)
            cursor = conn.cursor()
            query = f"SELECT * FROM public.auth_project where id = {decoded['project_id']}"
            cursor.execute(query)
            records = cursor.fetchall()
            selectObject = []
            columnNames = [column[0] for column in cursor.description]
            for record in records:
                selectObject.append(dict(zip(columnNames, record)))
            return selectObject[0]
    except Exception as e:
        response_return.set_error_status('Exception Occurred {}'.format(e))
