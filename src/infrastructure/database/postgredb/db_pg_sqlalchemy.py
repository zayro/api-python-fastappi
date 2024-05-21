from json import dumps
from icecream import ic
from sqlalchemy import MetaData, Table, create_engine, select, text


engine = create_engine(
    "postgresql+psycopg2://postgres:zayro@127.0.0.1/enterprise", future=True
)

"""
with engine.connect() as connection:
    metadata = MetaData()
    table = Table("prueba", metadata, schema="demo", autoload_with=engine)
    # Seleccionar un campo específico a mostrar
    stmt = select(table.c.name).limit(5)
    result = connection.execute(stmt).fetchall()
    results_as_dict = [dict(row) for row in result]
    for row in result:
        print(row)
"""


with engine.connect() as conn:
    execute = conn.execute(
        text("SELECT id::text, name, phone FROM demo.prueba limit 10")
    )
    ic()
    # Obtener todos los resultados como una lista de diccionarios
    result = execute.fetchall()

    # Convertir la fila a un diccionario
    if result:
        for row in result:
            print(row)
            # print(dict([row]))
    else:
        row_dict = {}


# from sqlalchemy import create_engine, select

# print(sqlalchemy.__version__)
