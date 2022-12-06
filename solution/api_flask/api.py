import json
import logging
from flask import Flask
from context_manager import conn_context_pg
from db_settings import db_set

app = Flask('sber_test')

logging.basicConfig(
    level=logging.INFO,
    filename="api_log.log",
    filemode="w")


def load_data_from_db(pg_conn, target):
    """
    Load data from db and return values for json response.
    """
    pg_curs = pg_conn.cursor()
    # query = f'''
    #     SELECT (id, code, name, address)
    #     FROM content.departments
    #     WHERE address LIKE '%.{target},%'
    #     ORDER BY id;'''
    query = f'''
        SELECT (id, code, name, address)
        FROM content.departments
        WHERE city='{target}'
        ORDER BY id;'''
    pg_curs.execute(query)
    values = []
    for row in pg_curs:
        split_row = row[0][1:-1].replace('"', '').split(',')
        id = split_row[0]
        code = split_row[1]
        name = split_row[2]
        st_idx = len(id) + len(code) + len(name) + 7
        address = row[0][st_idx:-2]
        values.append({
            'id': id,
            'code': code,
            'name': name,
            'address': address,
            })
    return values


@app.route('/api/list/<city>', methods=['GET'])
def index(city):
    target = city
    with conn_context_pg(db_set) as pg_conn:
        values = load_data_from_db(pg_conn, target)
    data_to_json = {
        'response': {
            'api': 'v1',
            'page': 'list',
            'values': values
        }
    }
    data_to_sent = json.dumps(data_to_json)
    return data_to_sent


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
