from dataclasses import dataclass
import mariadb
import sys

 
# Initialize Pool

pool = mariadb.ConnectionPool(
pool_name = 'demo',
pool_size = 3,
pool_reset_connection = False,
host='127.0.0.1',
user='root',
password='zayro',
port=3306,
database = 'demo'
)

def conectar(db): 
    try:
        
        print(db)
 
        conn = pool.get_connection()
        #conn.autocommit = True

        print('Conected Successfuly')
        return conn.cursor()        

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    except mariadb.PoolError  as e:
        print(f"PoolError connecting to MariaDB Platform: {e}")
    finally: 
        # Close Connection
        print('finally')
        conn.close()        
    

cur1 =  conectar('demo')

try:
    cur1.execute(
    "Select SLEEP (1), nombre From prueba", 
    ())
    print(cur1.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")


cur1 =  conectar('demo')
try:
    cur1.execute(
    "Select SLEEP (1), nombre From prueba", 
    ())
    print(cur1.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")




cur1 =  conectar('demo')
try:
    cur1.execute(
    "Select SLEEP (1), nombre From prueba ", 
    ())
    print(cur1.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")

