import psycopg2
from decouple import AutoConfig
config = AutoConfig()

DATABASE_CONFIG = {
    'dbname': config('DB_NAME'),
    'user': config('DB_USER'),
    'password': config('DB_PASSWORD'),
    'host': config('DB_HOST'),
    'port': config('DB_PORT')
}

def get_connection():
    return psycopg2.connect(**DATABASE_CONFIG)
# получим датафрейм по всем записям
def get_total_records():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM vw_tmp_import")
            return cursor.fetchone()[0]
# получим конкретную порцию данных со смещением для вывода в пагинатор
def get_records(limit, offset):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM vw_tmp_import LIMIT {limit} OFFSET {offset}")
            return cursor.fetchall()
# получим список серверов для выпадающего меню
def get_servers():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT server_name FROM servers")
            return [row[0] for row in cursor.fetchall()]
