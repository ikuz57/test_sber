from api_flask.context_manager import conn_context_pg
from api_flask.db_settings import db_settings
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--f', help='file_path')


def main():
    with conn_context_pg(db_settings) as pg_conn:
        curs = pg_conn.cursor()
        args = parser.parse_args()
        file_path = ''
        with open(args.f) as f:
            file_path = f.read()
        query = file_path
        curs.execute(query)


if __name__ == '__main__':
    main()
