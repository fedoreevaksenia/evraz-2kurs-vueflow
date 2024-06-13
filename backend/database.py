import psycopg2
from enviroments import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        self.conn.autocommit = True

    def query(self, request, params = []):
        try:
            cursor = self.conn.cursor()
            if len(params) == 0:
                cursor.execute(request)
            else:
                cursor.execute(request, params)

            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            json_result = [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None
        return json_result

    def release(self):
        self.conn.close()
