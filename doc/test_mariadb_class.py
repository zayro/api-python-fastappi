
import mariadb

class Database:

    cursor: mariadb.Cursor
    conn: mariadb.ConnectionPool    

  
    def __init__(self, db):
        try: 
            print("Init DB")
            # Connect to MariaDB Platform
            self.pool = mariadb.ConnectionPool(
            pool_name = db,
            pool_size = 1,
            pool_reset_connection = False,
            host='127.0.0.1',
            user='root',
            password='zayro',
            port=3306,
            database = db
            )

            self.conn = self.pool.get_connection()
            #conn.autocommit = True

            print('Conected Successfuly')


        except mariadb.PoolError  as e:
            print(f"PoolError connecting to MariaDB Platform: {e}")
            #self.conn.close()
        except mariadb.DatabaseError:
            print(f"Error connecting to MariaDB Platform: {e}")
        finally:            
            print('Close Connection finally')
            #self.conn.close()
                    

    def __del__(self):
        print('Destructor called ')
 

    def get_results(self): 
        desc = [d[0] for d in self.cursor.description]
        results = [dict(zip(desc, res)) for res in self.cursor.fetchall()]
        return results

    def select(self, sql: str, params: tuple):
        try:
            self.cursor.execute(sql, params)
            return self.get_results()
        except mariadb.Error as e:
            print(f"Error: {e}")
            # raise Exception("Error Sql")
            return False

    def execute(self,  sql: str, params: tuple = ()):
        try:
            self.cursor.execute(sql, params)
            if self.cursor.rowcount > 0:
                result = self.cursor.fetchall()    
                return result 
            else: 
                return None
            
        except mariadb.Error as e:
            print(f"Error: {e}")
            self.conn.close()
            return None

    def query(self,  sql: str, params: tuple = ()):
        try:
            self.cursor.execute(sql, params)
            return self.get_results()
        except mariadb.Error as e:
            print(f"Error: {e}")
            # raise Exception("Error Sql")
            return False

    def search(self, FIELDS, FROM: str, WHERE=None):

        str_fields = ','.join(map(str, FIELDS))

        # convert_where = [" = ".join(map(convert_string_quotes, item)) for item in list(WHERE.items())]

        if WHERE is not None:
            parse_text: str = ""
            for k, v in WHERE.items():
                if isinstance(v, str):
                    parse_text += k + ' = ' + f"'{v}'" + ' AND '
                else:
                    parse_text += k + ' = ' + f"{v}" + ' AND '
            str_where = parse_text.rsplit(' AND ', 1)[0]
            sql = f"SELECT {str_fields} FROM {FROM} WHERE {str_where} "
            print(sql)
            response = self.query(sql, ())
            return response
        else:
            sql = f"SELECT {str_fields} FROM {FROM}"
            print(sql)
            response = self.query(sql, ())
            return response
 
 
db = Database('demo')

cur1=db.conn.cursor()

try:
    cur1.execute(
    "SELECT * from prueba", 
    ())
    print(cur1.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")

cur2=db.conn.cursor()

try:
    cur2.execute(
    "SELECT * from prueba", 
    ())
    print(cur2.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")

cur33=db.conn.cursor()

try:
    cur33.execute(
    "SELECT * from prueba", 
    ())
    print(cur33.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")

db.conn.cursor()
db.conn.cursor()
db.conn.cursor()

db = Database('auth')

cur3=db.conn.cursor()

try:
    cur3.execute(
    "SELECT * from users", 
    ())
    print(cur3.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")



cur4=db.conn.cursor()

try:
    cur4.execute(
    "SELECT * from users", 
    ())
    print(cur4.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")



cur5=db.conn.cursor()

try:
    cur5.execute(
    "SELECT * from users", 
    ())
    print(cur5.fetchall())
except mariadb.Error as e:
    print(f"Error: {e}")
