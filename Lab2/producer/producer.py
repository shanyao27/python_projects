import os
import json
import argparse
from kafka import KafkaProducer
from common import config

def load_json_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("JSON должен быть объектом {table, schema, rows}")

    table = data["table"]
    schema = data["schema"]
    rows = data["rows"]

    return table, schema, rows

# python объекты - JSON файл
def make_message(table_name, schema, rows): 
    return json.dumps({
        'table': table_name,
        'schema': schema,
        'rows': rows,
    }).encode('utf-8')
