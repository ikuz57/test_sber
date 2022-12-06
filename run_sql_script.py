from db.context_manager import conn_context_pg
from db.db_settings import db_settings
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--f', help='file_path')


def main():
    file_data = ''
    args = parser.parse_args()    
    with open(args.f) as f:
        file_data = f.read()
    with conn_context_pg(db_settings) as pg_conn:
        curs = pg_conn.cursor()
        query = file_data
        curs.execute(query)
        pg_conn.commit()

if __name__ == '__main__':
    main()
