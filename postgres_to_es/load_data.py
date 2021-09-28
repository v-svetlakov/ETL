import psycopg2
import time
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config import dsl, es_conf
from postgresloader import PostgresLoader
from utils import backoff
# from es import EsSaver
import pprint

pp = pprint.PrettyPrinter(indent=4)


def load_from_postgres(pg_conn: _connection, state_bd=False) -> list:
    """Основной метод загрузки данных из Postgres"""
    postgres_saver = PostgresLoader(pg_conn, state_bd)
    data = postgres_saver.loader()
    return data


if __name__ == '__main__':
    # @backoff()
    def query_postgres():
        with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_pq = load_from_postgres(pg_conn, state_bd=True)
        pg_conn.close()
        return load_pq


    print(query_postgres())
    # def save_elastic():
    #     a = EsSaver(es_conf, query_postgres())
    #     print(a.load())
    #
    # save_elastic()
