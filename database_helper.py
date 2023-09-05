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
# получим общее количество записей
def get_total_records(server_name=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            if server_name: # если сервер указан выводим записи только по нему
                cursor.execute(
                    "SELECT COUNT(*) FROM vw_tmp_import WHERE server_name = %s",
                    (server_name,)
                )
            else:
                cursor.execute(  # иначе выводим количество всех строк датафрейма
                    "SELECT COUNT(*) FROM vw_tmp_import"
                )
            return cursor.fetchone()[0]

def get_records(server_name, owner_name, limit, offset):
    """
     ф. обрабатывает все возможные комбинации выбора сервера и владельца:
    1. Ни сервер, ни владелец не выбраны: выводятся все записи.
    2. Выбран только сервер: выводятся записи только для этого сервера.
    3. Выбран только владелец: выводятся записи только для этого владельца.
    4. Выбраны и сервер, и владелец: выводятся записи только для этой комбинации сервера и владельца.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            if server_name == "ALL" or not server_name:
                if owner_name and owner_name != "ALL":
                    query = f"SELECT * FROM vw_tmp_import WHERE full_name_owner = %s LIMIT {limit} OFFSET {offset}"
                    cursor.execute(query, (owner_name,))
                else:
                    query = f"SELECT * FROM vw_tmp_import LIMIT {limit} OFFSET {offset}"
                    cursor.execute(query)
            else:
                if owner_name and owner_name != "ALL":
                    query = f"SELECT * FROM vw_tmp_import WHERE server_name = %s AND full_name_owner = %s LIMIT {limit} OFFSET {offset}"
                    cursor.execute(query, (server_name, owner_name))
                else:
                    query = f"SELECT * FROM vw_tmp_import WHERE server_name = %s LIMIT {limit} OFFSET {offset}"
                    cursor.execute(query, (server_name,))
            return cursor.fetchall()



# получим список серверов для выпадающего меню
def get_servers():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT server_name FROM vw_tmp_import")
            return cursor.fetchall()
# получии список владельцев для выпадающего меню
def get_owners():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT full_name_owner FROM vw_tmp_import")
            return cursor.fetchall()
