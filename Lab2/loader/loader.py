import json
import time
import argparse
from kafka import KafkaConsumer 
import psycopg2 
from psycopg2 import sql 
from common import config 

def ensure_table(conn, table_name, columns): 
    with conn.cursor() as cur:
        cols_defs = [sql.SQL("{} TEXT").format(sql.Identifier(c)) for c in columns]
        q = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(cols_defs)
        )
        cur.execute(q)
    conn.commit()

def insert_rows(conn, table_name, columns, rows):
    with conn.cursor() as cur:
        cols = sql.SQL(', ').join(sql.Identifier(c) for c in columns)
        vals_p = sql.SQL(', ').join(sql.Placeholder() * len(columns))
        ins = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(sql.Identifier(table_name), cols, vals_p)
        for r in rows:
            cur.execute(ins, [r.get(c) for c in columns])
    conn.commit()

#адрес кафка-брокера, группа потребителей, топики, строка подключения к psql
def main(bootstrap, group, topics, pg_dsn):
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap,
        group_id=group,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=1000
    )
    conn = psycopg2.connect(pg_dsn)
    try:
        while True:
            consumed = False
            for msg in consumer:
                consumed = True
                payload = json.loads(msg.value.decode())
                table = payload['table']
                rows = payload['rows']

                if 'schema' in payload:
                    schema = payload['schema']
                else:
                    schema = list(rows[0].keys())
                ensure_table(conn, table, schema)
                insert_rows(conn, table, schema, rows)
                print(f'Loaded {len(rows)} rows into {table}')
            if not consumed:
                time.sleep(1)
    finally:
        consumer.close()
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap', default=config.KAFKA_LOCAL)
    parser.add_argument('--group', default='etl_loader_group')
    parser.add_argument('--topics', nargs='*', default=[])
    parser.add_argument('--pg', default=config.POSTGRES_DSN)
    args = parser.parse_args()
    if not args.topics:
        print('Specify topics.')
    else:
        main(args.bootstrap, args.group, args.topics, args.pg)
