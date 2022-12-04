from flask import Flask, request
from context_manager import conn_context_pg, sb_settings
import json
from dataclasses import asdict


app = Flask('sber_test')


def load_data_from_db(pg_conn, target):
    pg_curs = pg_conn.cursor()
    pg_curs.execute(f'''
        SELECT (id, code, name, address)
        FROM content.departments
        WHERE address LIKE '%.{target},%'
        ORDER BY id;''')
    data_to_send = []
    for row in pg_curs:
        #DictCursor не работает -_- не победил.
        split_row = row[0][1:-1].replace('"','').split(',')
        address = ''
        for i in range(3, len(split_row)):
            address += split_row[i]
        id = split_row[0]
        code = split_row[1]
        name = split_row[2]
        data_to_send.append({
            'id': id,
            'code': code,
            'name':name,
            'address':address,
            })
    return data_to_send


@app.route('/api/list/<city>', methods=['GET'])
def index(city):
    target = city
    with conn_context_pg(sb_settings) as pg_conn:
        data = load_data_from_db(pg_conn, target)
        data_to_json = {
            'response': {
                'api': 'v1',
                'page': 'list',
                'values': data
            }
        }
        data_to_sent = json.dumps(data_to_json)
    return data_to_sent


if __name__ == "__main__":
    app.run()
