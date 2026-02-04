import json
import sys

INVALID_CHARS = set('%#!@^&$:"\' ,.')

def validate(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # корень - объект
    if not isinstance(data, dict):
        raise ValueError('root must be an object')

    # проверка полей
    required_fields = ['table', 'schema', 'rows']
    for field in required_fields:
        if field not in data:
            raise ValueError(f'missing field: {field}')

    # проверка имени табл
    table_name = data['table']
    if not isinstance(table_name, str):
        raise ValueError('field "table" must be str')
    if any(c in INVALID_CHARS for c in table_name):
        raise ValueError(f'invalid character in table name: "{table_name}"')
    if table_name[0].isdigit():
        raise ValueError(f'table name cannot start with a digit: "{table_name}"')

    # проверка имен колонок
    schema = data['schema']
    if not isinstance(schema, list) or not all(isinstance(col, str) for col in schema):
        raise ValueError('field "schema" must be a list of sts')
    for col in schema:
        if any(c in INVALID_CHARS for c in col):
            raise ValueError(f'invalid character in column name: "{col}"')
        if col[0].isdigit():
            raise ValueError(f'column name cannot start with a digit: "{col}"')

    # проверка rows
    rows = data['rows']
    if not isinstance(rows, list):
        raise ValueError('field "rows" must be a list')
    for i, r in enumerate(rows, start=1):
        if not isinstance(r, dict):
            raise ValueError(f'row {i} must be an object')
        if set(r.keys()) != set(schema):
            raise ValueError(f'row {i} keys {list(r.keys())} do not match schema {schema}')

    print('OK:', path)
