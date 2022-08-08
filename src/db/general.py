# Module Imports
import mariadb


def convert_string_quotes(value: tuple):
    print('**************', value)
    return " = ".join('"%s"' % i for i in value)


def unique_keys(data: list[dict]):
    return ", ".join(str(item) for item in data[0].keys())


def values_dict(data: list[dict]):
    response = ""
    for item in data:
        response += "("
        for data in item.values():
            response += f'"{data}", '
        response += f")"

    response = response.replace(", )", '),')
    response = response[:-1]

    return response


class Database:

    cursor: mariadb.Cursor
    conn: mariadb.ConnectionPool    

  
    def __init__(self, db):
        
        print("Init DB")
        self.db =  db
        self.conn = mariadb.ConnectionPool(
        pool_name = self.db,
        pool_size = 2,
        pool_reset_connection = True,
        host='127.0.0.1',
        user='root',
        password='zayro',
        port=3306,
        database = self.db,
        )     
                    
        # Connect to MariaDB Platform
                  

    def __del__(self):
        print('Destructor called, Employee deleted.')
        self.cursor.close()
        self.conn.close() 
        
    def connectar(self):       
        try: 
            #conn.autocommit = True

            conn = self.conn.get_connection()
            print('Conected Successfuly')  
            self.cursor =  conn.cursor()        
            return  self.cursor 
            
        except mariadb.PoolError  as e:
            print(f"Error connecting to MariaDB Platform: {e}")    
            conn.close()
        except mariadb.DatabaseError:
            print("The database has gone away -- reconnecting.")  
            conn.close()
        finally:
            print("finally Connect Db.")  
            conn.close()        
        

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
                self.cursor.close()
                self.conn.close()
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

    def insert(self, TABLE: str, VALUES: list):

        fields: str = unique_keys(VALUES)
        values: str = values_dict(VALUES)

        sql = f"INSERT INTO {TABLE} ({fields})  VALUES {values} "
        print(sql)
        try:
            self.cursor.execute(sql)
            return [True, "Insert Success"]
        except mariadb.Error as e:
            print(f"Error: {e}")
            # raise Exception("Error Sql")
            return [False, f"Error: {e}"]


data = [{"nombre": "zayro",  "apellido": "gng", "info": '[{ "name" : "marlon" }]'},
        {"nombre": "barajas",  "apellido": "fer",  "info": '[{ "name" : "marlon" }]'}]


"""
# Get Cursor

sql = "SELECT username, ? FROM users where id_users =  ? "
params = ('email', 1,)
results = select(cur, sql, params)


print("The variable, name is of type:", type(results))
print(results)


for res in results:
    print(res)

"""
