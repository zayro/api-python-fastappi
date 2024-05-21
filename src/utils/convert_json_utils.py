import datetime


def sql_data(data: list):
    result = [convertir_a_json(row) for row in data]
    # json_data = json.dumps(result, sort_keys=True)
    return result


def convertir_a_json(valor):
    if isinstance(valor, datetime.datetime):
        return valor.isoformat()
    elif isinstance(valor, bytes):
        return valor.decode("utf-8")
    elif isinstance(valor, dict):
        return {key: convertir_a_json(v) for key, v in valor.items()}
    elif isinstance(valor, list):
        return [convertir_a_json(v) for v in valor]
    else:
        return valor
