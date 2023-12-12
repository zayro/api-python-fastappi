
"""Imports."""
import sys
from medoo import Medoo


class Database:
    # For other arguments, please refer to the original connect function of each client.
    def __init__(self):
        print("Init DB")
        try:
            self.conn = Medoo(
                dbtype="pgsql",
                user="postgres",
                password="zayro",
                host="localhost",
                database="enterprise",
                port=5432,
                logging=True,
            )
        except TypeError as e:
            print("----- TypeError Database ----- ")
            print(str(e))
            print("---------- ")
        except Exception as e:
            print("----- Exception Database ----- ")
            print(
                type(e).__name__,          # TypeError
                __file__,                  # /tmp/example.py
                e.__traceback__.tb_lineno  # 2
            )
            print(str(e))
            print("---------- ")
            sys.exit()
            return "error"

   # Calling destructor
    def __del__(self):
        print("Destructor Database.db called")
        self.conn.close()

    def select(self, table, field="*"):
        rs = self.conn.select(table, field)
        print(rs.export("json"))
        return rs.export("json")

    def search(self, table, fields, where=None):

        if type(fields) is list:
            field = ", ".join(fields)
        else:
            field = fields

        if where is not None and type(where) is dict:
            condition = where

        else:
            condition = None

        return self.conn.select(table, field, condition)

    def query(self, stm):
        rs = self.conn.query(stm, commit=True)
        # print(rs.export("json"))
        return rs

    def log(self):
        rs = self.conn.log()
        print(rs)

    def error(self):
        rs = self.conn.error()
        print(rs)

    def close(self):
        self.conn.close()
