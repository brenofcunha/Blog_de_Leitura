from django.db import connection


def execute_query(query: str, params=None):
    params = params or []
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    return []
