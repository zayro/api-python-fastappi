# Module Imports
from pickle import FALSE
import mariadb
import sys
import json


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="zayro",
        host="127.0.0.1",
        port=3306,
        database="auth"

    )
    print('connect successfuly')
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


def get_results(db_cursor):
    desc = [d[0] for d in db_cursor.description]
    results = [dict(zip(desc, res)) for res in db_cursor.fetchall()]
    return results


def select(db_cursor, sql: str, params: tuple):
    try:
        db_cursor.execute(sql, params)
        return get_results(cur)
    except mariadb.Error as e:
        print(f"Error: {e}")
        #raise Exception("Error Sql")
        return FALSE


def search(FIELDS, FROM: str, WHERE: dict, ORDER):
    str_fields = ','.join(map(str, FIELDS))
    print(str_fields)

    convert_where = [' = '.join(map(str, item)) for item in WHERE.items()]
    str_where = ' AND '.join(convert_where)

    sql = f"SELECT {str_fields} FROM {FROM} WHERE {str_where} "
    print(sql)

def insert(INSERT: str, VALUES):
    str_fields = ','.join(map(str, FIELDS))
    print(str_fields)

    convert_where = [' = '.join(map(str, item)) for item in WHERE.items()]
    str_where = ' AND '.join(convert_where)

    sql = f"SELECT {str_fields} FROM {FROM} WHERE {str_where} "
    print(sql)


search(['username, email'], 'users', { "id": 10, "username": "zayros"}, '')

# Get Cursor
cur = conn.cursor()

print(type(cur))
sql = "SELECT username, ? FROM users where id_users =  ? "
params = ('email', 1,)
results = select(cur, sql, params)


print("The variable, name is of type:", type(results))
print(results)


for res in results:
    print(res)


 


conn.close()

sys.exit(1)
