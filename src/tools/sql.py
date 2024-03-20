# Import JSON module
from typing import Optional


class SqlTools:

    def __init__(self, database):
        self.database = database

    def select(
        self,
        table: str,
        fields: list,
        where: Optional[dict] = None,
        order: Optional[dict] = None,
        limit: Optional[int] = None,
    ) -> str:

        if isinstance(fields, list):
            # list_field = ", ".join([str(elem) for elem in fields])
            list_field = ", ".join(fields)

        query = f"SELECT {list_field} FROM {table}"

        i = 0

        if where is not None:
            for i, (key, value) in enumerate(where.items()):
                if i == 0:
                    query += " WHERE "
                else:
                    query += " AND "
                query += "{}='{}'".format(key, value)

        if order is not None:
            for i, (key, value) in enumerate(order.items()):
                if i == 0:
                    query += " ORDER BY "
                else:
                    query += " , "
                query += "{} {}".format(key, value)

        if limit is not None:
            query += f" LIMIT {limit}"

        query += ";"
        return query

    def insert(self, table: str, data: list):
        query = f"INSERT INTO {table} "
        keys = []
        values = []
        for dic in data:
            for i, (key, value) in enumerate(dic.items()):
                if i == 0:
                    keys.append(key)
                    values.append(value)
                else:
                    values.append(value)

        query += "({}) values ('{}')".format(", ".join(keys), "', '".join(values))
        query += ";"
        return query


def filter(table, fields: list, **kwargs):

    if type(fields) is list:
        # list_field = ", ".join([str(elem) for elem in fields])
        list_field = ", ".join(fields)

    query = f"SELECT {list_field} FROM {table}"

    i = 0

    for key, value in kwargs.items():
        if i == 0:
            query += " WHERE "
        else:
            query += " AND "
        query += "{}='{}'".format(key, value)
        i += 1
    query += ";"
    return query


info_filter = filter(table="clientes", fields=["nombre", "apellido"], ciudad="Madrid")


def pruebas_insert():
    table = "demo"

    data = [
        {"nombre": "pepe", "apellido": "grillo"},
        {"nombre": "marlon", "apellido": "arias"},
    ]

    db = SqlTools("pg")
    info_insert_v1 = db.insert(table=table, data=data)
    print(info_insert_v1)


def pruebas_select():
    db = SqlTools("pg")
    table = "clientes"
    fields = ["nombre", "apellido"]
    where = {"nombre": "token", "apellido": "arias"}
    order = {"estado": "ASC"}
    limit = 10

    info_filter_v1 = db.select(table, fields)
    info_filter_v2 = db.select(table, fields, where)
    info_filter_v3 = db.select(table=table, fields=fields, where=where, order=order)
    info_filter_v4 = db.select(
        table=table, fields=fields, where=where, order=order, limit=limit
    )

    print(info_filter_v1)
    print(info_filter_v2)
    print(info_filter_v3)
    print(info_filter_v4)


pruebas_select()
pruebas_insert()
