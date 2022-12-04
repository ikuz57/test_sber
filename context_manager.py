from psycopg2 import connect as pg_connect
from contextlib import contextmanager
from psycopg2.extras import DictCursor


sb_settings = {
    'dbname': 'sber_test',
    'user': 'app',
    'password': '123',
    'host': 'localhost',
    'port': 5432,
    'options': '-c search_path=content',
}

@contextmanager
def conn_context_pg(config: dict):
    conn_pg = pg_connect(**config, cursor_factory=DictCursor)
    yield conn_pg
    conn_pg.close()
