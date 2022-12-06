from solution.context_manager import conn_context_pg
from solution.db_settings import db_set
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--f', help='file_path')


def main():
    file_data = ''
    args = parser.parse_args()
    with open(args.f) as f:
        file_data = f.read()
    with conn_context_pg(db_set) as pg_conn:
        curs = pg_conn.cursor()
        query = file_data
        curs.execute(query)
        pg_conn.commit()


if __name__ == '__main__':
    main()
