""" Import JSON module """

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
        """
        Generate a SELECT query based on the provided parameters.

        Args:
            table (str): The name of the table to select from.
            fields (list): The list of fields to select.
            where (Optional[dict], optional): The WHERE clause as a dictionary of column-value pairs. Defaults to None.
            order (Optional[dict], optional): The ORDER BY clause as a dictionary of column-direction pairs. Defaults to None.
            limit (Optional[int], optional): The LIMIT clause specifying the maximum number of rows to return. Defaults to None.

        Returns:
            str: The generated SELECT query.
        """
        if isinstance(fields, list):
            list_field = ", ".join(fields)
        else:
            list_field = "*"

        query = f"SELECT {list_field} FROM {table}"

        if where is not None:
            query += " WHERE " + " AND ".join(
                [f"{key}='{value}'" for key, value in where.items()]
            )

        if order is not None:
            query += " ORDER BY " + ", ".join(
                [f"{key} {value}" for key, value in order.items()]
            )

        if limit is not None:
            query += f" LIMIT {limit}"

        query += ";"
        return query

    def generate_insert_query(self, table_name: str, data: dict) -> str:
        try:
            # Validar que table_name no esté vacío
            if not table_name:
                raise ValueError("El nombre de la tabla no puede estar vacío.")

            # Validar que data sea un diccionario
            if not isinstance(data, dict):
                raise TypeError("Los datos deben ser un diccionario.")

            # Validar que data no esté vacío
            if not data:
                raise ValueError("El diccionario de datos no puede estar vacío.")

            # Crear la lista de columnas y valores a partir del diccionario de datos
            columns = ", ".join(data.keys())
            values = ", ".join([f"'{value}'" for value in data.values()])

            # Crear la consulta SQL
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

            # Imprimir el string de la consulta SQL
            print(query)
            return query

        except (TypeError, ValueError) as e:
            print(f"Error: {e}")

    def generate_insert_query_multiple(self, table_name: str, data: list):
        try:
            # Validar que table_name no esté vacío
            if not table_name:
                raise ValueError("El nombre de la tabla no puede estar vacío.")

            # Validar que data sea una lista de diccionarios o un solo diccionario
            if not isinstance(data, (dict, list)):
                raise TypeError(
                    "Los datos deben ser un diccionario o una lista de diccionarios."
                )

            # Si data es un diccionario, convertirlo a una lista con un solo diccionario
            if isinstance(data, dict):
                data = [data]

            # Verificar si data está vacío
            if not data:
                raise ValueError(
                    "El diccionario o lista de datos no puede estar vacío."
                )

            # Crear la lista de columnas a partir del primer registro
            columns = ", ".join(data[0].keys())

            # Crear la lista de valores para múltiples registros
            values_list = []
            for record in data:
                values = ", ".join([f"'{value}'" for value in record.values()])
                values_list.append(f"({values})")

            # Unir todos los conjuntos de valores en una sola instrucción
            values_str = ", ".join(values_list)

            # Crear la consulta SQL de inserción múltiple
            query = f"INSERT INTO {table_name} ({columns}) VALUES {values_str};"

            # Imprimir el string de la consulta SQL
            print(query)
            return query

        except (TypeError, ValueError) as e:
            print(f"Error: {e}")

    def insert_multiples_stament(self, table: str, data: list) -> str:
        query = f"INSERT INTO {table} "
        common_keys = set(data[0].keys())
        query += "({}) values ".format(", ".join(common_keys))
        for dic in data:
            placeholders = ", ".join(["%s"] * len(dic))
            query += f"({placeholders}), "
        query = query.rstrip(", ")
        return query + ";"

    def insert_multiples(self, table: str, data: list):
        query = f"INSERT INTO {table} "
        common_keys = set(data[0].keys())
        query += "({}) values ".format(", ".join(common_keys))
        for dic in data:
            query += " ('{}'), ".format("', '".join(dic.values()))

        query = query.rstrip(", ")
        query += ";"
        return query

    def filter(self, table, fields: list, **kwargs):

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
